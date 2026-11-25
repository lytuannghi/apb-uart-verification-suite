import os
import subprocess
from agents.eda_runner import _resolve_tool


class EDARunner:
    def __init__(self, iverilog_path=None):
        self.iverilog_bin = _resolve_tool("iverilog", iverilog_path)
        self.vvp_bin = _resolve_tool("vvp", iverilog_path)

    def compile_and_simulate(self, rtl_path: str, tb_path: str, vvp_out: str = "output/sim.vvp"):
        """Compiles RTL and Testbench using iverilog -Wall, then simulates with vvp."""
        os.makedirs(os.path.dirname(vvp_out) or ".", exist_ok=True)
        compile_cmd = [self.iverilog_bin, "-Wall", "-g2005", "-o", vvp_out, rtl_path, tb_path]
        try:
            compile_res = subprocess.run(compile_cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", check=False)
            if compile_res.returncode != 0:
                return False, f"[COMPILE ERROR]:\n{compile_res.stderr}\n{compile_res.stdout}"
        except Exception as e:
            return False, f"[IVERILOG ERROR]: {str(e)}"

        try:
            sim_res = subprocess.run([self.vvp_bin, vvp_out], capture_output=True, text=True, encoding="utf-8", errors="replace", check=False)
            output_log = (sim_res.stdout or "") + ("\n" + sim_res.stderr if sim_res.stderr else "")
            lower_log = output_log.lower()
            if "error" in lower_log or "fail" in lower_log or "fatal" in lower_log or sim_res.returncode != 0:
                return False, f"[SIM ERROR]:\n{output_log}"
            return True, f"[SIM PASS]:\n{output_log}"
        except Exception as e:
            return False, f"[VVP ERROR]: {str(e)}"


if __name__ == "__main__":
    runner = EDARunner()
    print("iverilog:", runner.iverilog_bin)
    print("vvp:", runner.vvp_bin)
