# ============================================================================
# Agent 6: EDA Runner & Self-Healing Lead
# Author: Lý Tuấn Nghi (lytuannghi) & Multi-Agent IC Design Team
# ============================================================================

import subprocess
import os
import shutil

class EDARunner:
    """Agent 6: Interacts with Icarus Verilog and vvp simulation engine."""

    def __init__(self, iverilog_path=r"D:\CODE\GGANTIGRAVITY\iverilog\bin"):
        self.iverilog_bin = os.path.join(iverilog_path, "iverilog.exe")
        self.vvp_bin = os.path.join(iverilog_path, "vvp.exe")

        if not os.path.exists(self.iverilog_bin):
            self.iverilog_bin = shutil.which("iverilog") or "iverilog"
        if not os.path.exists(self.vvp_bin):
            self.vvp_bin = shutil.which("vvp") or "vvp"

    def run_simulation(self, rtl_files, tb_file, vvp_out="output/apb_uart_sim.vvp"):
        """
        Compiles all RTL files and Testbench, executes simulation,
        and parses Pass/Fail metrics.
        """
        os.makedirs(os.path.dirname(vvp_out), exist_ok=True)

        # 1. Compile Phase
        cmd_compile = [self.iverilog_bin, "-g2005", "-o", vvp_out] + rtl_files + [tb_file]
        try:
            res_comp = subprocess.run(cmd_compile, capture_output=True, text=True, check=False)
            if res_comp.returncode != 0:
                return False, f"[COMPILATION ERROR]:\n{res_comp.stderr}"
        except Exception as e:
            return False, f"[EDA EXECUTION ERROR]: {str(e)}"

        # 2. Simulation Phase
        try:
            res_sim = subprocess.run([self.vvp_bin, vvp_out], capture_output=True, text=True, check=False)
            output = res_sim.stdout + ("\n" + res_sim.stderr if res_sim.stderr else "")
            
            # Check if simulation passed all testcases
            if "VERIFICATION PASSED" in output and "[FAIL]" not in output:
                return True, output
            else:
                return False, output
        except Exception as e:
            return False, f"[VVP SIMULATION ERROR]: {str(e)}"

if __name__ == "__main__":
    runner = EDARunner()
    print("EDA Runner initialized. iverilog:", runner.iverilog_bin)
