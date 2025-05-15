from assets.VGraphParser import VGraphParser
from assets.VGraphVisitor import VGraphVisitor


class VariableSymbol:
    """
    Represents a variable symbol in the symbol table
    """
    def __init__(self, name, vtype, initialized=False):
        self.name = name
        self.type = vtype  # 'int', 'color', 'bool'
        self.initialized = initialized
        self.used = False


class FunctionSymbol:
    def __init__(self, name, param_types):
        self.name = name
        self.param_types = param_types  # list of types


class SymbolTable:
    """
    Represents a symbol table for variable declarations and scopes
    """
    def __init__(self):
        self.scopes = [{}]  # stack of scopes

    def enter_scope(self):
        self.scopes.append({})

    def exit_scope(self):
        return self.scopes.pop()

    def declare(self, name, symbol):
        if name in self.scopes[-1]:
            return False  # already declared in current scope
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
    """
    Handles lexical analysis of code
    """
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.errors = []
        self.warnings = []
        self.current_function = None

    # Entry point: entire program
    def visitProgram(self, ctx: VGraphParser.ProgramContext):
        self.visitChildren(ctx)
        # Check for unused variables
        for symbol in self.symbol_table.get_all_symbols():
            if not symbol.used:
                self.warnings.append(f"Warning: variable '{symbol.name}' declared but never used")
        return None

    def visitBlock(self, ctx: VGraphParser.BlockContext):
        self.symbol_table.enter_scope()
        self.visitChildren(ctx)
        self.symbol_table.exit_scope()
        return None
    
    def visitDeclaration(self, ctx: VGraphParser.DeclarationContext):
        vtype = ctx.TYPE().getText()
        for id_token in ctx.ID():
            name = id_token.getText()

            # Identifier validation
            if not name[0].islower() or len(name) > 15:
                self.errors.append(f"Invalid identifier: '{name}'")
                continue

            # Check for redeclaration in the same scope
            if not self.symbol_table.declare(name, VariableSymbol(name, vtype)):
                self.errors.append(f"Redeclaration of variable: '{name}'")
        return None
    
    def visitFunctionDeclaration(self, ctx: VGraphParser.FunctionDeclarationContext):
        name = ctx.ID().getText()
        param_list = ctx.parameterList()
        param_types = [t.getText() for t in param_list.TYPE()] if param_list else []
        param_ids = [i.getText() for i in param_list.ID()] if param_list else []

        if not self.symbol_table.declare_function(name, param_types):
            self.errors.append(f"Redeclaration of function: '{name}'")
            return None

        # Enter function scope
        self.symbol_table.enter_scope()
        self.current_function = name

        # Declare parameters in the new scope
        for vtype, vname in zip(param_types, param_ids):
            self.symbol_table.declare(vname, VariableSymbol(vname, vtype, initialized=True))

        self.visit(ctx.block())

        # Exit function scope
        self.current_function = None
        self.symbol_table.exit_scope()
        return None

    def visitAssignment(self, ctx: VGraphParser.AssignmentContext):
        name = ctx.ID().getText()
        symbol = self.symbol_table.lookup(name)
        if not symbol:
            self.errors.append(f"Undeclared variable: '{name}'")
        else:
            expr_type = self.evaluate_expression_type(ctx.expression())
            if expr_type and expr_type != symbol.type:
                self.errors.append(f"Type mismatch: cannot assign {expr_type} to variable '{name}' of type {symbol.type}")
            else:
                symbol.initialized = True
        return self.visitChildren(ctx)
    
    def evaluate_expression_type(self, expr):
        if expr.INT():
            return "int"
        elif expr.BOOL():
            return "bool"
        elif expr.COLOR():
            return "color"
        elif expr.ID():
            name = expr.ID().getText()
            symbol = self.symbol_table.lookup(name)
            if not symbol:
                self.errors.append(f"Use of undeclared variable: '{name}'")
                return None
            symbol.used = True
            if not symbol.initialized:
                self.errors.append(f"Variable '{name}' used before initialization")
            return symbol.type
        elif expr.functionCall():
            return self.visitFunctionCall(expr.functionCall())
        elif expr.op:  # binary or unary operation
            left_type = self.evaluate_expression_type(expr.expression(0))
            if expr.getChildCount() == 1:  # unary operator (!)
                if expr.op.text == '!' and left_type != 'bool':
                    self.errors.append("Operator '!' can only be applied to boolean expressions")
                    return None
                return 'bool'
            right_type = self.evaluate_expression_type(expr.expression(1))
            op = expr.op.text

            if op in ['+', '-', '*', '/', '%']:
                if left_type != 'int' or right_type != 'int':
                    self.errors.append(f"Arithmetic operation not allowed between types {left_type} and {right_type}")
                    return None
                return 'int'
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
    
    def visitFunctionCall(self, ctx: VGraphParser.FunctionCallContext):
        fname = ctx.ID().getText()
        args = ctx.expression()
        arg_types = [self.evaluate_expression_type(arg) for arg in args]

        if fname in ["cos", "sin"]:
            if len(arg_types) != 1 or arg_types[0] != "int":
                self.errors.append(f"Function '{fname}' expects one int argument")
                return None
            return "int"
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
        
        # User-defined function
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
