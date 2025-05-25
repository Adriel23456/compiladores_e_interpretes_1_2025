from __future__ import annotations
import os
import traceback
from typing import Any

from config import BASE_DIR, CompilerData
from CompilerLogic.semanticAnalyzer import SymbolTable
from CompilerLogic.IRLogic.IRGenerator import IRGenerator
from CompilerLogic.RichSymbolAdapter import RichSymbolAdapter
class IntermediateCodeGenerator:
    """
    Llamada pública: `generate(output_path:str|None) -> str|None`
    """

    # ──────────────────────────────────────────
    @staticmethod
    def _as_symbol_table(raw: Any) -> SymbolTable:
        """
        Asegura que `raw` sea una instancia de SymbolTable.
        Si viene como dict (o None), lo envuelve.
        """
        return raw if isinstance(raw, SymbolTable) else SymbolTable(raw or {})

    # ──────────────────────────────────────────
    @classmethod
    def generate(cls, out_file: str | None = None) -> str | None:
        """
        Produce el texto IR.  
        Devuelve None si:
          • existen errores semánticos pendientes
          • faltan AST o parser
          • ocurre una excepción durante la generación
        """
        # 1. abortar si ya hay errores de semántica
        if CompilerData.semantic_errors:
            return None

        # 2. obtener artefactos previos
        tree   = CompilerData.ast
        parser = CompilerData.parser
        if tree is None or parser is None:
            return None

        simple_symtab: SymbolTable = cls._as_symbol_table(CompilerData.symbol_table)
        rich_symtab = RichSymbolAdapter(simple_symtab)

        # 3. intentar producir el IR
        try:
            ir_text: str = IRGenerator(tree, rich_symtab, parser).generate()
        except Exception as err:  # pylint: disable=broad-except
            traceback.print_exc()
            return None

        # 4. guardar el resultado
        if out_file is None:
            out_file = os.path.join(BASE_DIR, "out", "vGraph.ll")

        os.makedirs(os.path.dirname(out_file), exist_ok=True)
        with open(out_file, "w", encoding="utf-8") as fh:
            fh.write(ir_text)

        return ir_text