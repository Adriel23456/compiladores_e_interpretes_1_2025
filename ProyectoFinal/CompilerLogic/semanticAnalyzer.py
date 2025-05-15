from assets.VGraphParser import VGraphParser
from assets.VGraphVisitor import VGraphVisitor
from config import BASE_DIR, ASSETS_DIR, CompilerData, States

class VariableSymbol:
    def __init__(self, name, vtype, initialized=False):
        self.name = name
        self.type = vtype
        self.initialized = initialized
        self.used = False

class FunctionSymbol:
    def __init__(self, name, param_types):
        self.name = name
        self.param_types = param_types

class SymbolTable:
    def __init__(self):
        self.scopes = [{}]
        self.functions = {}

    def enter_scope(self):
        self.scopes.append({})

    def exit_scope(self):
        return self.scopes.pop()

    def declare(self, name, symbol):
        if name in self.scopes[-1]:
            return False
        self.scopes[-1][name] = symbol
        return True

    def lookup(self, name):
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        return None

    def declare_function(self, name, param_types):
        if name in self.functions:
            return False
        self.functions[name] = FunctionSymbol(name, param_types)
        return True

    def get_function(self, name):
        return self.functions.get(name, None)

    def get_all_symbols(self):
        return [symbol for scope in self.scopes for symbol in scope.values()]

class SemanticAnalyzer(VGraphVisitor):
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.errors = []
        self.warnings = []
        self.current_function = None
        self.ast = CompilerData.ast
        self.color_constants = {"rojo", "azul", "verde", "negro", "blanco"}

    def run(self):
        self.visit(self.ast)
        CompilerData.semantic_errors = self.errors
        CompilerData.enhanced_symbol_table = self.symbol_table.get_all_symbols()

    def visitProgram(self, ctx: VGraphParser.ProgramContext):
        self.visitChildren(ctx)
        for symbol in self.symbol_table.get_all_symbols():
            if isinstance(symbol, VariableSymbol) and not symbol.used:
                self.warnings.append(f"Warning: variable '{symbol.name}' declared but never used")
        return None

    def visitBlock(self, ctx: VGraphParser.BlockContext):
        self.symbol_table.enter_scope()
        self.visitChildren(ctx)
        self.symbol_table.exit_scope()
        return None

    def visitDeclaration(self, ctx: VGraphParser.DeclarationContext):
        vtype_ctx = ctx.typeDeclaration().vartype()
        vtype = vtype_ctx.getText()
        if ctx.ID():
            names = [ctx.ID().getText()]
        elif ctx.idList():
            names = [id_token.getText() for id_token in ctx.idList().ID()]
        else:
            names = []
        for name in names:
            if not name[0].islower() or len(name) > 15:
                self.errors.append(f"Invalid identifier: '{name}'")
                continue
            if not self.symbol_table.declare(name, VariableSymbol(name, vtype)):
                self.errors.append(f"Redeclaration of variable: '{name}'")
        return None

    def visitFunctionDeclStatement(self, ctx: VGraphParser.FunctionDeclStatementContext):
        name = ctx.ID().getText()
        param_list = ctx.paramList()
        param_ids = [i.getText() for i in param_list.ID()] if param_list else []
        param_types = ["int"] * len(param_ids)

        if not self.symbol_table.declare_function(name, param_types):
            self.errors.append(f"Redeclaration of function: '{name}'")
            return None

        self.symbol_table.enter_scope()
        self.current_function = name

        for vtype, vname in zip(param_types, param_ids):
            self.symbol_table.declare(vname, VariableSymbol(vname, vtype, initialized=True))

        self.visit(ctx.block())

        self.current_function = None
        self.symbol_table.exit_scope()
        return None

    def visitAssignmentStatement(self, ctx: VGraphParser.AssignmentStatementContext):
        return self.visit(ctx.assignmentExpression())

    def visitAssignmentExpression(self, ctx: VGraphParser.AssignmentExpressionContext):
        name = ctx.ID().getText()
        symbol = self.symbol_table.lookup(name)
        if not symbol:
            self.errors.append(f"Undeclared variable: '{name}'")
        else:
            expr_type = self.evaluate_expression_type(ctx.expr())
            if expr_type and expr_type != symbol.type:
                self.errors.append(f"Type mismatch: cannot assign {expr_type} to variable '{name}' of type {symbol.type}")
            else:
                symbol.initialized = True
        return None

    def visitReturnStatement(self, ctx):
        if self.current_function is None:
            self.errors.append("Return statement outside of a function")
        self.evaluate_expression_type(ctx.expression())
        return None

    def evaluate_expression_type(self, expr):
        ctx_name = type(expr).__name__

        if ctx_name == "NumberExprContext":
            value = expr.getText()
            if "." in value:
                return "float"
            return "int"

        if ctx_name == "ColorExprContext":
            return "color"

        if ctx_name == "BoolLiteralExprContext":
            return "bool"

        if ctx_name == "IdExprContext":
            name = expr.getText()
            if name in self.color_constants:
                return "color"
            symbol = self.symbol_table.lookup(name)
            if not symbol:
                self.errors.append(f"Use of undeclared variable: '{name}'")
                return None
            symbol.used = True
            if not symbol.initialized:
                self.errors.append(f"Variable '{name}' used before initialization")
            return symbol.type

        if ctx_name in ["SinExprContext", "CosExprContext"]:
            arg_type = self.evaluate_expression_type(expr.expr())
            if arg_type is None:
                return None
            if arg_type not in ["int", "float"]:
                self.errors.append(f"Function '{ctx_name[:-11].lower()}' expects numeric argument, got {arg_type}")
                return None
            return "float"

        if hasattr(expr, "op") and expr.op:
            left_type = self.evaluate_expression_type(expr.expr(0))
            right_type = self.evaluate_expression_type(expr.expr(1)) if expr.getChildCount() > 1 else None

            if left_type is None or right_type is None:
                return None

            op = expr.op.text
            if op in ['+', '-', '*', '/', '%']:
                if left_type not in ['int', 'float'] or right_type not in ['int', 'float']:
                    self.errors.append(f"Arithmetic operation not allowed between types {left_type} and {right_type}")
                    return None
                return 'int' if left_type == right_type == 'int' else 'float'
            elif op in ['<', '>', '<=', '>=']:
                if left_type != 'int' or right_type != 'int':
                    self.errors.append(f"Comparison not allowed between types {left_type} and {right_type}")
                    return None
                return 'bool'
            elif op in ['==', '!=']:
                if left_type != right_type:
                    self.errors.append(f"Equality comparison between different types: {left_type} and {right_type}")
                    return None
                return 'bool'
            elif op in ['&&', '||']:
                if left_type != 'bool' or right_type != 'bool':
                    self.errors.append(f"Logical operation not allowed between types {left_type} and {right_type}")
                    return None
                return 'bool'

        return None

    def visitFunctionCall(self, ctx):
        fname = ctx.ID().getText()
        args = ctx.expression()
        arg_types = [self.evaluate_expression_type(arg) for arg in args]

        if fname in ["cos", "sin"]:
            if len(arg_types) != 1 or arg_types[0] not in ["int", "float"]:
                self.errors.append(f"Function '{fname}' expects one numeric argument")
                return None
            return "float"
        elif fname == "setcolor":
            if len(arg_types) != 1 or arg_types[0] != "color":
                self.errors.append("Function 'setcolor' expects one color argument")
                return None
            return None
        elif fname.startswith("draw"):
            if not all(arg == "int" for arg in arg_types):
                self.errors.append(f"Drawing function '{fname}' expects only int arguments")
                return None
            return None

        fdecl = self.symbol_table.get_function(fname)
        if not fdecl:
            self.errors.append(f"Call to undefined function '{fname}'")
            return None
        if len(arg_types) != len(fdecl.param_types):
            self.errors.append(f"Function '{fname}' expects {len(fdecl.param_types)} arguments but got {len(arg_types)}")
            return None
        for expected, actual in zip(fdecl.param_types, arg_types):
            if expected != actual:
                self.errors.append(f"Function '{fname}' argument type mismatch: expected {expected}, got {actual}")
                return None
        return None

    def reportErrors(self):
        if not self.errors:
            print("[✔] Semantic analysis completed with no errors.")
        else:
            print("[✘] Semantic errors detected:")
            for err in self.errors:
                print("  -", err)

        if self.warnings:
            print("[!] Warnings:")
            for warn in self.warnings:
                print("  -", warn)