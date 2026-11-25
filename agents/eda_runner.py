# ============================================================================
# Agent 6: EDA Runner & Self-Healing Lead
# Author: Ly Tuan Nghi (lytuannghi) & Multi-Agent IC Design Team
# ============================================================================

import os
import shutil
import subprocess


def _resolve_tool(exe_name, custom_dir=None):
    found = shutil.which(exe_name)
    if found:
        return found
    candidates = []
    if custom_dir:
        candidates.append(os.path.join(custom_dir, exe_name))
        candidates.append(os.path.join(custom_dir, exe_name + ".exe"))
    env_bin = os.environ.get("IVERILOG_BIN")
    if env_bin:
        candidates.append(os.path.join(env_bin, exe_name))
        candidates.append(os.path.join(env_bin, exe_name + ".exe"))
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sibling_bin = os.path.join(os.path.dirname(repo_root), "iverilog", "bin")
    candidates.append(os.path.join(sibling_bin, exe_name))
    candidates.append(os.path.join(sibling_bin, exe_name + ".exe"))
    for c in candidates:
        if os.path.exists(c):
            return c
    return exe_name


class EDARunner:
    """Agent 6: Interacts with Icarus Verilog and vvp simulation engine."""

    def __init__(self, iverilog_path=None):
        self.iverilog_bin = _resolve_tool("iverilog", iverilog_path)
        self.vvp_bin = _resolve_tool("vvp", iverilog_path)

    def run_simulation(self, rtl_files, tb_file, vvp_out="output/apb_uart_sim.vvp"):
        """
        Compiles all RTL files and Testbench with -Wall, executes simulation,
        and parses Pass/Fail metrics.
        """
        os.makedirs(os.path.dirname(vvp_out) or ".", exist_ok=True)

        cmd_compile = [self.iverilog_bin, "-Wall", "-g2005", "-o", vvp_out] + rtl_files + [tb_file]
        try:
            res_comp = subprocess.run(cmd_compile, capture_output=True, text=True, encoding="utf-8", errors="replace", check=False)
            if res_comp.returncode != 0:
                return False, f"[COMPILATION ERROR]:\n{res_comp.stderr}\n{res_comp.stdout}"
            if res_comp.stderr.strip():
                return False, f"[COMPILER WARNINGS (-Wall)]:\n{res_comp.stderr}"
        except Exception as e:
            return False, f"[EDA EXECUTION ERROR]: {str(e)}"

        try:
            res_sim = subprocess.run([self.vvp_bin, vvp_out], capture_output=True, text=True, encoding="utf-8", errors="replace", check=False)
            output = (res_sim.stdout or "") + ("\n" + res_sim.stderr if res_sim.stderr else "")
            if "VERIFICATION PASSED" in output and "[FAIL]" not in output and res_sim.returncode == 0:
                return True, output
            return False, output
        except Exception as e:
            return False, f"[VVP SIMULATION ERROR]: {str(e)}"


if __name__ == "__main__":
    runner = EDARunner()
    print("EDA Runner initialized. iverilog:", runner.iverilog_bin)
