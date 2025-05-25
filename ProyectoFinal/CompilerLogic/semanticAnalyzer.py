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
        self.color_constants = {"rojo", "azul", "verde", "negro", "blanco"}
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

    def evaluate_expression_type(self, expr):
        ctx_name = type(expr).__name__
        node_id = str(id(expr))

        children = []
        if hasattr(expr, 'expr'):
            expr_children = expr.expr()
            if not isinstance(expr_children, list):
                expr_children = [expr_children]
            for child in expr_children:
                if child:
                    self.evaluate_expression_type(child)
                    children.append(str(id(child)))

        inferred_type = "unknown"
        if ctx_name == "NumberExprContext":
            value = expr.getText()
            inferred_type = "float" if "." in value else "int"
        elif ctx_name == "ColorExprContext":
            inferred_type = "color"
        elif ctx_name == "BoolLiteralExprContext":
            inferred_type = "bool"
        elif ctx_name == "IdExprContext":
            name = expr.getText()
            symbol = self.symbol_table.lookup(name)
            if not symbol:
                self.errors.append(f"Use of undeclared variable: '{name}'")
            else:
                symbol.used = True
                if not symbol.initialized:
                    self.errors.append(f"Variable '{name}' used before initialization")
                inferred_type = symbol.type

        self.enriched_tree[node_id] = {
            "text": expr.getText(),
            "type": inferred_type,
            "ctx": ctx_name,
            "children": children
        }
        return inferred_type

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
