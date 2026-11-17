import os
import sys
from dotenv import load_dotenv
from agents import ArchitectAgent, RTLDesignerAgent, VerificationAgent
from eda_runner import EDARunner

load_dotenv()

def run_project(user_request: str):
    print("=" * 60)
    print("🚀 BẮT ĐẦU QUY TRÌNH THIẾT KẾ VI MẠCH TỰ ĐỘNG BẰNG ĐỘI NGŨ AI")
    print("=" * 60)
    print(f"📌 Yêu cầu bài toán: {user_request}\n")

    os.makedirs("output", exist_ok=True)
    architect = ArchitectAgent()
    designer = RTLDesignerAgent()
    verifier = VerificationAgent()
    eda = EDARunner()

    # Bước 1: Architect Agent lên đặc tả kỹ thuật
    print("[1/4] 🧠 Agent 1 (Architect) đang phân tích kiến trúc và lập spec...")
    spec = architect.design_spec(user_request)
    with open("output/spec.md", "w", encoding="utf-8") as f:
        f.write(spec)
    print("✅ Đã hoàn thành bản đặc tả kỹ thuật -> Lưu tại: output/spec.md\n")

    # Bước 2: RTL Designer viết Verilog
    print("[2/4] 💻 Agent 2 (RTL Designer) đang viết mã nguồn Verilog...")
    rtl_code = designer.generate_rtl(spec)
    with open("output/module.v", "w", encoding="utf-8") as f:
        f.write(rtl_code)
    print("✅ Đã sinh mã Verilog -> Lưu tại: output/module.v\n")

    # Bước 3: Verification Engineer viết Testbench
    print("[3/4] 🔬 Agent 3 (Verification) đang viết Testbench kiểm thử...")
    tb_code = verifier.generate_testbench(spec, rtl_code)
    with open("output/module_tb.v", "w", encoding="utf-8") as f:
        f.write(tb_code)
    print("✅ Đã sinh Testbench -> Lưu tại: output/module_tb.v\n")

    # Bước 4: EDA Runner chạy mô phỏng và vòng lặp tự sửa lỗi (Self-Healing Loop)
    print("[4/4] ⚙️ Agent 4 (EDA Runner) đang biên dịch với Icarus Verilog và mô phỏng...")
    max_retries = 3
    attempt = 0
    success = False

    while attempt < max_retries:
        attempt += 1
        print(f"--- Thử nghiệm mô phỏng lần {attempt}/{max_retries} ---")
        success, message = eda.compile_and_simulate("output/module.v", "output/module_tb.v")
        
        print(message)
        if success:
            print("\n🎉 XUẤT SẮC! Thiết kế đã vượt qua tất cả bài kiểm tra mô phỏng!")
            break
        else:
            print(f"\n⚠️ Phát hiện lỗi! Đang gửi log lỗi ngược về cho Agent 2 (RTL Designer) để tự sửa...")
            rtl_code = designer.generate_rtl(spec, error_feedback=message)
            with open("output/module.v", "w", encoding="utf-8") as f:
                f.write(rtl_code)
            # Tạo lại testbench nếu cần hoặc thử lại
            tb_code = verifier.generate_testbench(spec, rtl_code)
            with open("output/module_tb.v", "w", encoding="utf-8") as f:
                f.write(tb_code)

    print("\n" + "=" * 60)
    if success:
        print("🏆 DỰ ÁN HOÀN THÀNH THÀNH CÔNG:")
        print("  - Bản vẽ Spec:       output/spec.md")
        print("  - Mã nguồn RTL:      output/module.v")
        print("  - Testbench:         output/module_tb.v")
        if os.path.exists("output/waveform.vcd"):
            print("  - Dạng sóng Waveform: output/waveform.vcd (Mở bằng GTKWave)")
    else:
        print("❌ Chưa vượt qua kiểm thử sau các lần thử. Hãy kiểm tra file log.")
    print("=" * 60)

if __name__ == "__main__":
    prompt = "Thiết kế bộ đếm nhị phân 4-bit với xung clk, tín hiệu reset bất đồng bộ tích cực mức cao, tín hiệu enable cho phép đếm, và cờ overflow khi đếm tới 15."
    if len(sys.argv) > 1:
        prompt = " ".join(sys.argv[1:])
    run_project(prompt)
