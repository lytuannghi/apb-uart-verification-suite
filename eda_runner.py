import subprocess
import os
import shutil

class EDARunner:
    def __init__(self, iverilog_path=r"D:\CODE\GGANTIGRAVITY\iverilog\bin"):
        self.iverilog_bin = os.path.join(iverilog_path, "iverilog.exe")
        self.vvp_bin = os.path.join(iverilog_path, "vvp.exe")
        
        # Fallback to PATH if custom path not found
        if not os.path.exists(self.iverilog_bin):
            self.iverilog_bin = shutil.which("iverilog") or "iverilog"
        if not os.path.exists(self.vvp_bin):
            self.vvp_bin = shutil.which("vvp") or "vvp"

    def compile_and_simulate(self, rtl_path: str, tb_path: str, vvp_out: str = "output/sim.vvp"):
        """
        Compiles RTL and Testbench using iverilog, then simulates with vvp.
        Returns: (success: bool, message: str)
        """
        os.makedirs(os.path.dirname(vvp_out), exist_ok=True)
        
        # Step 1: Compile with iverilog
        compile_cmd = [self.iverilog_bin, "-g2005", "-o", vvp_out, rtl_path, tb_path]
        try:
            compile_res = subprocess.run(
                compile_cmd,
                capture_output=True,
                text=True,
                check=False
            )
            if compile_res.returncode != 0:
                return False, f"[LỖI BIÊN DỊCH IVERILOG]:\n{compile_res.stderr}\n{compile_res.stdout}"
        except Exception as e:
            return False, f"[LỖI KHI GỌI IVERILOG]: {str(e)}"

        # Step 2: Simulate with vvp
        sim_cmd = [self.vvp_bin, vvp_out]
        try:
            sim_res = subprocess.run(
                sim_cmd,
                capture_output=True,
                text=True,
                check=False
            )
            output_log = sim_res.stdout + ("\n" + sim_res.stderr if sim_res.stderr else "")
            
            # Check for standard simulation failure signs
            lower_log = output_log.lower()
            if "error" in lower_log or "fail" in lower_log or "fatal" in lower_log or sim_res.returncode != 0:
                return False, f"[LỖI MÔ PHỎNG VVP]:\n{output_log}"
            
            return True, f"[MÔ PHỎNG THÀNH CÔNG]:\n{output_log}"
        except Exception as e:
            return False, f"[LỖI KHI CHẠY VVP]: {str(e)}"

if __name__ == "__main__":
    runner = EDARunner()
    print("EDA Runner initialized successfully.")
    print("iverilog:", runner.iverilog_bin)
    print("vvp:", runner.vvp_bin)
