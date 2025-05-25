from __future__ import annotations

import os
import traceback
from typing import Optional

from llvmlite import binding as llvm
from config import BASE_DIR


# inicialización global LLVM: cuesta milisegundos, se hace 1 vez
llvm.initialize()
llvm.initialize_native_target()
llvm.initialize_native_asmprinter()


class Optimizer:
    """Método público:  `optimize(ir_text:str, out_file:str|None) -> str|None`"""

    # -----------------------------------------------------------------
    @staticmethod
    def _build_passmanager(opt_level: int = 2) -> llvm.ModulePassManager:
        """
        Crea un pass manager equivalente a `opt -O<opt_level>`.
        Para -O2/-Os típicos basta con InstructionCombining + GVN + CFGSimpl.
        """
        pmb = llvm.create_pass_manager_builder()
        pmb.opt_level  = opt_level          # 0–3
        pmb.size_level = 0                  # 0: normal, 1: -Os, 2: -Oz
        pmb.loop_vectorize = True
        pmb.slp_vectorize  = True

        pm = llvm.ModulePassManager()
        pmb.populate(pm)
        return pm

    # -----------------------------------------------------------------
    @classmethod
    def optimize(
        cls,
        ir_text: str,
        output_path: Optional[str] = None,
        opt_level: int = 2,
    ) -> Optional[str]:
        """
        Devuelve el IR optimizado o None si falla.
        Si `output_path` es None se escribe en “out/vGraph_opt.ll”.
        """

        try:
            # 1) Parsear el IR a un ModuleRef
            mod = llvm.parse_assembly(ir_text)
            mod.verify()

            # 2) Ejecutar los pases
            pm = cls._build_passmanager(opt_level)
            pm.run(mod)

            optimized = str(mod)

            # 3) Guardar si se pidió
            if output_path is None:
                output_path = os.path.join(BASE_DIR, "out", "vGraph_opt.ll")
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, "w", encoding="utf-8") as fh:
                fh.write(optimized)

            return optimized

        except Exception as exc:  # pylint: disable=broad-except
            # Puedes conectar esto con CompilerData.semantic_errors si lo deseas
            print("[IROptimizer] Error optimizando IR:")
            traceback.print_exc()
            return None
