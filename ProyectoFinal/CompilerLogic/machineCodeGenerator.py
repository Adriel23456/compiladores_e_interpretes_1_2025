import os
import traceback
from typing import Optional

from llvmlite import binding as llvm
from config import BASE_DIR, CompilerData



llvm.initialize()
llvm.initialize_native_target()
llvm.initialize_native_asmprinter()


class MachineCodeGenerator:
    """
    Toma un IR optimizado (LLVM IR) y genera su equivalente en ensamblador x86-64,
    almacenándolo en out/vGraph.asm y guardándolo en CompilerData.asm_code.
    """

    @classmethod
    def generate_asm(cls, ir_path: str = None, output_path: str = None) -> Optional[str]:
        try:
            # 1. Leer IR desde archivo (vGraph_opt.ll)
            if ir_path is None:
                ir_path = os.path.join(BASE_DIR, "out", "vGraph_opt.ll")
            if not os.path.exists(ir_path):
                print(f"[CodeGen] No se encontró el archivo IR en: {ir_path}")
                return None

            with open(ir_path, "r", encoding="utf-8") as fh:
                ir_text = fh.read()

            # 2. Parsear y verificar módulo IR
            mod = llvm.parse_assembly(ir_text)
            mod.verify()

            # 3. Obtener target machine
            target = llvm.Target.from_default_triple()
            target_machine = target.create_target_machine()

            # 4. Generar código ensamblador
            asm_code = target_machine.emit_assembly(mod)

            # 5. Filtrar caracteres no ASCII ni imprimibles
            cleaned_code = '\n'.join(
                ''.join(c if c.isascii() and c.isprintable() else ' ' for c in line)
                for line in asm_code.splitlines()
            )

            # 6. Guardar en archivo .asm
            if output_path is None:
                output_path = os.path.join(BASE_DIR, "out", "vGraph.asm")
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            with open(output_path, "w", encoding="utf-8") as out_f:
                out_f.write(cleaned_code)

            # 7. Guardar en CompilerData limpio
            CompilerData.asm_code = cleaned_code

            print(f"[CodeGen] Código ensamblador generado exitosamente en {output_path}")
            return cleaned_code

        except Exception:
            print("[CodeGen] Error durante la generación de código ensamblador:")
            traceback.print_exc()
            return None
