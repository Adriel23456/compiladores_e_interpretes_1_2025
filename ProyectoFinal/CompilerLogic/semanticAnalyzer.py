from assets.VGraphParser import VGraphParser
from assets.VGraphVisitor import VGraphVisitor
from config import BASE_DIR, ASSETS_DIR, CompilerData, States
import pydot
import os

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
        self.color_constants = {"rojo", "azul", "verde", "negro", "blanco", "cyan", "magenta", "amarillo", 'marrón'}
        self.enriched_tree = {}

        images_dir = os.path.join(ASSETS_DIR, "Images")
        if not os.path.exists(images_dir):
            os.makedirs(images_dir)
        self.semantic_tree_path = os.path.join(images_dir, "semantic_tree.png")

    def run(self):
        self.visit(self.ast)
        CompilerData.semantic_errors = self.errors
        CompilerData.enhanced_symbol_table = self.symbol_table.get_all_symbols()
        CompilerData.semantic_tree = self.enriched_tree
        self.generate_semantic_tree_image(self.semantic_tree_path)
        CompilerData.semantic_tree_path = self.semantic_tree_path

        for symbol in self.symbol_table.get_all_symbols():
            if isinstance(symbol, VariableSymbol) and not symbol.used and not symbol.initialized:
                self.warnings.append(f"Warning: variable '{symbol.name}' declared but never used")

    def visitProgram(self, ctx: VGraphParser.ProgramContext):
        self.visitChildren(ctx)
        return None

    def visitBlock(self, ctx: VGraphParser.BlockContext):
        self.symbol_table.enter_scope()
        self.visitChildren(ctx)
        self.symbol_table.exit_scope()
        return None

    def visitDeclaration(self, ctx: VGraphParser.DeclarationContext):
        vtype_ctx = ctx.typeDeclaration().vartype()
        vtype = vtype_ctx.getText()
        line = ctx.start.line
        if ctx.ID():
            names = [ctx.ID().getText()]
        elif ctx.idList():
            names = [id_token.getText() for id_token in ctx.idList().ID()]
        else:
            names = []
        for name in names:
            if not name[0].islower() or len(name) > 15:
                self.errors.append(f"Line {line}: Invalid identifier: '{name}'")
                continue
            if not self.symbol_table.declare(name, VariableSymbol(name, vtype)):
                self.errors.append(f"Line {line}: Redeclaration of variable: '{name}'")
        return None

    def visitFunctionDeclStatement(self, ctx: VGraphParser.FunctionDeclStatementContext):
        name = ctx.ID().getText()
        param_list = ctx.paramList()
        param_ids = [i.getText() for i in param_list.ID()] if param_list else []
        param_types = ["int"] * len(param_ids)
        line = ctx.start.line

        # 1. Verificar redeclaración (funciones globales)
        if self.symbol_table.get_function(name):
            self.errors.append(f"Line {line}: Redeclaration of function: '{name}'")
            return None

        # 2. Declarar la función antes de entrar al bloque (soporte recursivo)
        self.symbol_table.declare_function(name, param_types)

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

    def visitAssignmentExpression(self, ctx):
        name = ctx.ID().getText()
        line = ctx.start.line
        symbol = self.symbol_table.lookup(name)
        if not symbol:
            self.errors.append(f"Line {line}: Undeclared variable: '{name}'")
        else:
            symbol.initialized = True
            expr_type = self.evaluate_expression_type(ctx.expr())
            if expr_type and expr_type != symbol.type:
                if symbol.type == "int" and expr_type == "float":
                    self.warnings.append(f"Line {line}: Implicit cast from float to int in assignment to '{name}'")
                else:
                    self.errors.append(f"Line {line}: Type mismatch: cannot assign {expr_type} to variable '{name}' of type {symbol.type}")
        return None
    
    def visitReturnStatement(self, ctx):
        line = ctx.start.line
        if self.current_function is None:
            self.errors.append(f"Line {line}: Return statement outside of a function")
        try:
            self.evaluate_expression_type(ctx.expr())
        except AttributeError:
            try:
                self.evaluate_expression_type(ctx.returnExpr())
            except AttributeError:
                self.errors.append(f"Line {line}: Return statement must return a value")
        return None

    def evaluate_expression_type(self, expr):
        if hasattr(expr, 'typeCast') and expr.typeCast():
            target_type = expr.typeCast().getText()
            inner_expr = expr.expr()
            inner_type = self.evaluate_expression_type(inner_expr)
            if target_type == "int" and inner_type == "float":
                return "int"
            elif target_type == inner_type:
                return target_type
            else:
                self.errors.append(f"Invalid cast from {inner_type} to {target_type}")
                return 'unknown'

        line = expr.start.line if hasattr(expr, 'start') else 'unknown'
        ctx_name = type(expr).__name__
        node_id = str(id(expr))
        children = []
        inferred_type = None

        if ctx_name == "NumberExprContext":
            inferred_type = "float" if "." in expr.getText() else "int"
        elif ctx_name == "ColorExprContext":
            if hasattr(expr, 'expr') and expr.expr():
                inferred_type = self.evaluate_expression_type(expr.expr())
            elif hasattr(expr, 'ID') and expr.ID():
                name = expr.ID().getText()
                symbol = self.symbol_table.lookup(name)
                if symbol:
                    symbol.used = True
                    if not symbol.initialized:
                        self.errors.append(f"Line {line}: Variable '{name}' used before initialization")
                    inferred_type = symbol.type
                elif name in self.color_constants:
                    inferred_type = "color"
                else:
                    self.errors.append(f"Line {line}: Use of undeclared variable or color constant: '{name}'")
                    return 'unknown'
            else:
                name = expr.getText()
                symbol = self.symbol_table.lookup(name)
                if symbol:
                    symbol.used = True
                    if not symbol.initialized:
                        self.errors.append(f"Line {line}: Variable '{name}' used before initialization")
                    inferred_type = symbol.type
                elif name in self.color_constants:
                    inferred_type = "color"
                else:
                    self.errors.append(f"Line {line}: Use of undeclared color constant: '{name}'")
                    return 'unknown'
        elif ctx_name == "BoolLiteralExprContext":
            inferred_type = "bool"
        elif ctx_name == "IdExprContext":
            name = expr.getText()
            symbol = self.symbol_table.lookup(name)
            if symbol:
                symbol.used = True
                if not symbol.initialized:
                    self.errors.append(f"Line {line}: Variable '{name}' used before initialization")
                inferred_type = symbol.type
            elif name in self.color_constants:
                inferred_type = "color"
            else:
                self.errors.append(f"Line {line}: Use of undeclared variable: '{name}'")
                return 'unknown'
        elif ctx_name in ["SinExprContext", "CosExprContext"]:
            arg_type = self.evaluate_expression_type(expr.expr())
            children.append(str(id(expr.expr())))
            if arg_type not in ["int", "float"]:
                self.errors.append(f"Line {line}: Function '{ctx_name[:-11].lower()}' expects numeric argument, got {arg_type}")
                return 'unknown'
            inferred_type = "float"
        elif ctx_name == "ParenExprContext":
            inferred_type = self.evaluate_expression_type(expr.expr())
        elif hasattr(expr, "op") and expr.op:
            left_type = self.evaluate_expression_type(expr.expr(0))
            right_type = self.evaluate_expression_type(expr.expr(1)) if expr.getChildCount() > 1 else None
            children.extend([str(id(expr.expr(0)))])
            if expr.getChildCount() > 1:
                children.extend([str(id(expr.expr(1)))])
            if left_type is None or right_type is None:
                return "unknown"
            op = expr.op.text
            if op in ['+', '-', '*', '/', '%']:
                if left_type not in ['int', 'float'] or right_type not in ['int', 'float']:
                    self.errors.append(f"Line {line}: Arithmetic operation not allowed between types {left_type} and {right_type}")
                    return 'unknown'
                inferred_type = 'int' if left_type == right_type == 'int' else 'float'
            elif op in ['<', '>', '<=', '>=']:
                if left_type != 'int' or right_type != 'int':
                    self.errors.append(f"Line {line}: Comparison not allowed between types {left_type} and {right_type}")
                    return 'unknown'
                inferred_type = 'bool'
            elif op in ['==', '!=']:
                if left_type != right_type:
                    self.errors.append(f"Line {line}: Equality comparison between different types: {left_type} and {right_type}")
                    return 'unknown'
                inferred_type = 'bool'
            elif op in ['&&', '||']:
                if left_type != 'bool' or right_type != 'bool':
                    self.errors.append(f"Line {line}: Logical operation not allowed between types {left_type} and {right_type}")
                    return 'unknown'
                inferred_type = 'bool'
            else:
                self.errors.append(f"Line {line}: Binary expression node does not have two operands.")
                return "unknown"
        elif hasattr(expr, 'expr') and callable(expr.expr):
            try:
                left_type = self.evaluate_expression_type(expr.expr(0))
                right_type = self.evaluate_expression_type(expr.expr(1))
                children.extend([str(id(expr.expr(0))), str(id(expr.expr(1)))])
                if left_type is None or right_type is None:
                    return 'unknown'
                if left_type not in ['int', 'float'] or right_type not in ['int', 'float']:
                    self.errors.append(f"Line {line}: Binary operation not allowed between types {left_type} and {right_type}")
                    return 'unknown'
                inferred_type = 'float' if 'float' in [left_type, right_type] else 'int'
            except Exception as e:
                self.errors.append(f"Line {line}: Unexpected error evaluating binary expression: {e}")
                return 'unknown'
        elif ctx_name == "FuncCallExprContext":
            fname = expr.ID().getText()
            arg_types = []
            if hasattr(expr, 'expr'):
                expr_children = expr.expr()
                if not isinstance(expr_children, list):
                    expr_children = [expr_children]
                for child in expr_children:
                    if child:
                        child_type = self.evaluate_expression_type(child)
                        if child_type is None:
                            return "unknown"
                        arg_types.append(child_type)
            else:
                arg_types.append("unknown")
            if fname in ["cos", "sin"]:
                for arg in arg_types:
                    if arg not in ["int", "float"]:
                        self.errors.append(f"Line {line}: Function '{fname}' expects numeric argument, got {arg}")
                        return 'unknown'
                inferred_type = "float"

        # 🆕 Ajuste final: recorre subexpresiones por defecto
        else:
            if hasattr(expr, 'expr') and callable(expr.expr):
                sub_exprs = expr.expr()
                if not isinstance(sub_exprs, list):
                    sub_exprs = [sub_exprs]
                for sub_expr in sub_exprs:
                    self.evaluate_expression_type(sub_expr)

        if inferred_type:
            self.enriched_tree[node_id] = {
                "text": expr.getText(),
                "type": inferred_type,
                "ctx": ctx_name,
                "children": children
            }

        return inferred_type

    def visitFunctionCall(self, ctx):
        fname = ctx.ID().getText()
        line = ctx.start.line
        arg_types = []

        def recursive_check_for_id(expr):
            if hasattr(expr, 'ID') and expr.ID():
                name = expr.ID().getText()
                symbol = self.symbol_table.lookup(name)
                if symbol:
                    symbol.used = True
                    if not symbol.initialized:
                        self.errors.append(f"Line {line}: Variable '{name}' used before initialization")
            if hasattr(expr, 'expr') and callable(expr.expr):
                sub_exprs = expr.expr()
                if not isinstance(sub_exprs, list):
                    sub_exprs = [sub_exprs]
                for sub_expr in sub_exprs:
                    recursive_check_for_id(sub_expr)

        if hasattr(ctx, 'expression'):
            args = ctx.expression()
            if not isinstance(args, list):
                args = [args]
            for arg in args:
                if arg:
                    arg_type = self.evaluate_expression_type(arg)
                    arg_types.append(arg_type)
                    recursive_check_for_id(arg)
        else:
            arg_types.append("unknown")

        if fname in ["cos", "sin"]:
            if len(arg_types) != 1 or arg_types[0] not in ["int", "float"]:
                self.errors.append(f"Line {line}: Function '{fname}' expects one numeric argument")
                return 'unknown'
            return "float"
        elif fname == "setcolor":
            if len(arg_types) != 1 or arg_types[0] != "color":
                self.errors.append(f"Line {line}: Function 'setcolor' expects one color argument")
                return 'unknown'
            return None
        elif fname.startswith("draw"):
            if not all(arg == "int" for arg in arg_types):
                self.errors.append(f"Line {line}: Drawing function '{fname}' expects only int arguments")
                return 'unknown'
            return None

        fdecl = self.symbol_table.get_function(fname)
        if not fdecl:
            self.errors.append(f"Line {line}: Call to undefined function '{fname}'")
            return 'unknown'
        if len(arg_types) != len(fdecl.param_types):
            self.errors.append(f"Line {line}: Function '{fname}' expects {len(fdecl.param_types)} arguments but got {len(arg_types)}")
            return 'unknown'
        for expected, actual in zip(fdecl.param_types, arg_types):
            if expected != actual:
                self.errors.append(f"Line {line}: Function '{fname}' argument type mismatch: expected {expected}, got {actual}")
                return 'unknown'
        return None

    def generate_semantic_tree_image(self, output_path):
        graph = pydot.Dot(graph_type='digraph', rankdir='TB')
        for node_id, data in self.enriched_tree.items():
            label = f"{data['ctx']}\n{data['text']}\n{data['type']}"
            graph.add_node(pydot.Node(node_id, label=label, shape='box'))
        for node_id, data in self.enriched_tree.items():
            for child in data.get('children', []):
                graph.add_edge(pydot.Edge(node_id, child))
        graph.write_png(output_path)

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
