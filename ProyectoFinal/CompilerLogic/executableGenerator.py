import os
import platform
import subprocess
import sys
import shutil

try:
    from config import BASE_DIR
except ImportError:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class ExecutableGenerator:
    def __init__(self, asm_path=None, runtime_obj_path=None, output_dir=None, exe_name="vGraph.exe"):
        self.platform = platform.system().lower()
        self.is_windows = self.platform == 'windows'
        self.is_linux = self.platform == 'linux'
        self.is_mac = self.platform == 'darwin'
        self.output_dir = output_dir or os.path.join(BASE_DIR, "out")
        self.asm_path = asm_path or os.path.join(self.output_dir, "vGraph.asm")
        self.obj_path = os.path.join(self.output_dir, "vGraph.o")
        self.exe_name = exe_name
        self.exe_path = os.path.join(self.output_dir, self.exe_name)
        self.runtime_dir = os.path.join(BASE_DIR, "CompilerLogic", "IRLogic")
        os.makedirs(self.runtime_dir, exist_ok=True)
        self.runtime_c_path = os.path.join(self.runtime_dir, "runtime.c")
        self.runtime_obj_path = runtime_obj_path or os.path.join(self.runtime_dir, f"runtime_{self.platform}.o")
        self.compiler = self._detect_compiler()
        os.makedirs(self.output_dir, exist_ok=True)
        if not os.path.exists(self.runtime_obj_path):
            self._compile_runtime()

    def _detect_compiler(self):
        for compiler in ['gcc', 'clang']:
            if shutil.which(compiler):
                return compiler
        raise EnvironmentError("No suitable compiler found. Please install GCC or Clang.")

    def _compile_runtime(self):
        cmd = [self.compiler, "-O2", "-fPIC", "-c", self.runtime_c_path, "-o", self.runtime_obj_path]
        try:
            os.makedirs(os.path.dirname(self.runtime_obj_path), exist_ok=True)
            subprocess.run(cmd, cwd=self.runtime_dir, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            raise

    def _ensure_final_newline(self, filepath):
        with open(filepath, 'rb+') as f:
            f.seek(-1, os.SEEK_END)
            last_char = f.read(1)
            if last_char != b'\n':
                f.write(b'\n')

    def assemble(self):
        self._ensure_final_newline(self.asm_path)
        cmd = [self.compiler, '-x', 'assembler', '-c', self.asm_path, '-o', self.obj_path]
        return self._run_command(cmd, "Assembly")

    def link(self):
        cmd = [self.compiler, self.obj_path, self.runtime_obj_path, '-o', self.exe_path]
        if self.is_linux:
            cmd.append('-no-pie')
        cmd.append('-lm')
        return self._run_command(cmd, "Linking")

    def build(self):
        success, msg = self.assemble()
        if not success:
            return False, msg
        success, msg = self.link()
        if not success:
            return False, msg
        return True, f"Executable created at {self.exe_path}"

    def _run_command(self, cmd, step_name):
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            if result.returncode != 0:
                return False, f"{step_name} failed:\n{result.stderr}"
            return True, f"{step_name} successful."
        except subprocess.TimeoutExpired:
            return False, f"{step_name} timed out."
        except Exception as e:
            return False, f"{step_name} error: {str(e)}"

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Generate .exe from .asm")
    parser.add_argument("--asm", help="Path to input .asm file")
    parser.add_argument("--runtime", help="Optional path to runtime object file")
    parser.add_argument("--output-dir", default="out", help="Directory to store output files")
    parser.add_argument("--exe-name", default="vGraph.exe", help="Name of the output executable")
    args = parser.parse_args()
    generator = ExecutableGenerator(
        asm_path=args.asm,
        runtime_obj_path=args.runtime,
        output_dir=args.output_dir,
        exe_name=args.exe_name
    )
    success, message = generator.build()
    print(message)
