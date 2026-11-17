import os
import re
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# List of models in order of priority / fallback
CANDIDATE_MODELS = [
    "gemini-3.1-flash-lite",
    "gemini-3.8-flash",
    "gemini-3.5-flash"
]

def generate_with_fallback(prompt: str, system_instruction: str, temperature: float = 0.2) -> str:
    """Generate content with automatic fallback across models if one is busy (503/429)."""
    last_err = None
    for model_name in CANDIDATE_MODELS:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=temperature
                )
            )
            if response and response.text:
                return response.text
        except Exception as e:
            last_err = e
            # Small delay before trying next model
            time.sleep(1)
            continue
    raise RuntimeError(f"Tất cả các model đều bận hoặc gặp lỗi: {last_err}")

def extract_code_block(text: str, lang: str = "verilog") -> str:
    """Extract code block from markdown output."""
    pattern = rf"```{lang}?\s*(.*?)```"
    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return text.strip()

class ArchitectAgent:
    """Agent 1: Hardware Architect - Designs specs, I/O ports, FSM."""
    
    SYSTEM_INSTRUCTION = """
    Bạn là một Hardware Architect (Kiến trúc sư phần cứng vi mạch) chuyên nghiệp.
    Khi người dùng đưa ra một ý tưởng hoặc yêu cầu module số (Digital Circuit):
    Nhiệm vụ của bạn:
    1. Xác định tên module (VD: counter_4bit, uart_tx, fifo_sync).
    2. Liệt kê rõ bảng chân tín hiệu (Inputs, Outputs, Bus Width).
    3. Mô tả nguyên lý hoạt động, máy trạng thái (FSM nếu có), điều kiện reset (sync hay async).
    4. Liệt kê các test cases quan trọng cần kiểm thử.
    Hãy trả lời rõ ràng, mạch lạc, có tính kỹ thuật cao.
    """

    def design_spec(self, user_prompt: str) -> str:
        return generate_with_fallback(user_prompt, self.SYSTEM_INSTRUCTION, temperature=0.2)

class RTLDesignerAgent:
    """Agent 2: RTL Designer - Writes Synthesizable Verilog Code."""

    SYSTEM_INSTRUCTION = """
    Bạn là một Senior RTL Design Engineer chuyên thiết kế vi mạch bằng Verilog/SystemVerilog.
    Nhiệm vụ của bạn là nhận bản đặc tả kỹ thuật (Spec) và viết mã Verilog chuẩn, synthesizable (tổng hợp được).
    Quy tắc bắt buộc:
    1. Chỉ sử dụng chuẩn Verilog-2001 synthesizable.
    2. Khai báo rõ ràng module name, ports (input/output/reg/wire) và độ rộng bit.
    3. Tuân thủ chuẩn coding: dùng non-blocking (<=) cho sequential logic, blocking (=) cho combinational logic.
    4. Toàn bộ mã nguồn Verilog phải nằm bên trong một khối markdown duy nhất: ```verilog ... ```. Không giải thích dông dài ngoài khối code.
    Nếu nhận được thông báo lỗi từ EDA simulation, bạn phải phân tích lỗi và viết lại mã Verilog đã sửa hoàn chỉnh.
    """

    def generate_rtl(self, spec_text: str, error_feedback: str = None) -> str:
        prompt = f"Bản đặc tả kỹ thuật module:\n{spec_text}\n"
        if error_feedback:
            prompt += f"\n[CẢNH BÁO: LẦN THỬ NGHIỆM TRƯỚC ĐÃ BỊ LỖI]:\n{error_feedback}\nHãy phân tích lỗi trên và cung cấp lại mã Verilog hoàn chỉnh đã được khắc phục."
        else:
            prompt += "\nHãy viết mã nguồn Verilog hoàn chỉnh cho module này."

        raw = generate_with_fallback(prompt, self.SYSTEM_INSTRUCTION, temperature=0.2)
        return extract_code_block(raw, "verilog")

class VerificationAgent:
    """Agent 3: Verification Engineer - Writes Verilog Testbench."""

    SYSTEM_INSTRUCTION = """
    Bạn là một Digital Verification Engineer (DV Engineer).
    Nhiệm vụ của bạn là viết Verilog Testbench (_tb.v) hoàn chỉnh để mô phỏng và kiểm tra tính đúng đắn của module RTL.
    Quy tắc bắt buộc cho Testbench:
    1. Tạo xung nhịp clock và reset đầy đủ.
    2. Khởi tạo tín hiệu bằng initial block.
    3. Thêm `$dumpfile("output/waveform.vcd");` và `$dumpvars(0, <tb_name>);` để lưu dạng sóng cho GTKWave.
    4. Thêm các kiểm tra tự động (self-checking assertions) bằng lệnh $display và nếu sai in rõ 'FAIL', nếu đúng in 'PASS'.
    5. Luôn kết thúc mô phỏng bằng `$finish;`.
    6. Toàn bộ mã Testbench phải nằm bên trong khối markdown: ```verilog ... ```. Không giải thích dông dài ngoài khối code.
    """

    def generate_testbench(self, spec_text: str, rtl_code: str) -> str:
        prompt = f"""
        Bản đặc tả module:
        {spec_text}

        Mã nguồn RTL đã viết:
        ```verilog
        {rtl_code}
        ```

        Hãy viết Testbench Verilog hoàn chỉnh để kiểm thử đầy đủ các chức năng và corner cases.
        """
        raw = generate_with_fallback(prompt, self.SYSTEM_INSTRUCTION, temperature=0.2)
        return extract_code_block(raw, "verilog")
