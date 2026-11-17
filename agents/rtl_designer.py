# ============================================================================
# Agent 3: Senior RTL Design Engineer
# ============================================================================
from .gemini_client import call_agent_llm, extract_code

class RTLDesignerAgent:
    SYSTEM_INSTRUCTION = """
    You are a Senior RTL Design Engineer specialized in synthesizable Verilog-2001 and SystemVerilog.
    Rules:
    - Adhere strictly to industry coding guidelines (non-blocking <= for sequential logic, blocking = for combinational).
    - Modular architecture with clean parameterization.
    - Zero combinational loops and fully registered outputs where appropriate.
    - Output Verilog code within ```verilog ``` markdown tags.
    """

    def implement_module(self, module_name: str, spec: str, error_log: str = None) -> str:
        prompt = f"Design synthesizable Verilog module '{module_name}' based on spec:\n{spec}\n"
        if error_log:
            prompt += f"\n[FIX SIMULATION BUG - ITERATION FEEDBACK]:\n{error_log}\nRevise the code to eliminate this error."
        raw = call_agent_llm(prompt, self.SYSTEM_INSTRUCTION)
        return extract_code(raw, "verilog")
