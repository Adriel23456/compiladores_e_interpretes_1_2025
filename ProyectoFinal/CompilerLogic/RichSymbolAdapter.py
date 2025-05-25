from CompilerLogic.semanticAnalyzer import SymbolTable
class RichSymbolAdapter:
    """
    Envuelve la SymbolTable simple y emula la API rica que espera el IRGenerator.
    No cambia la tabla original; solo traduce.
    """

    def __init__(self, simple_table: "SymbolTable"):
        self._tbl = simple_table

    # --- API mínima que usa el IRGenerator -------------------------
    def lookup(self, name, *_, **__):
        return self._tbl.lookup(name)

    def get_all_symbols(self):
        """
        Devuelve un dict por ámbito como espera el IRGenerator:
            {
              "global": { "x": {...}, ... },
              "<func>": { "param": {...}, ... }
            }
        """
        grouped = {}
        # 1) variables / params
        for scope_idx, scope in enumerate(self._tbl.scopes):
            scope_name = "global" if scope_idx == 0 else f"local{scope_idx}"
            grouped.setdefault(scope_name, {})
            for n, sym in scope.items():
                grouped[scope_name][n] = {
                    "type": getattr(sym, "type", "int"),
                    "line": getattr(sym, "line", 1),
                    "column": getattr(sym, "column", 0),
                    "initialized": getattr(sym, "initialized", True),
                    "used": getattr(sym, "used", False),
                    "scope": scope_name,
                }

        # 2) funciones
        for fname, f in self._tbl.functions.items():
            grouped["global"][fname] = {
                "type": "function",
                "line": getattr(f, "line", 1),
                "column": getattr(f, "column", 0),
            }
        return grouped