# ============================================================================
# Agent 4: Testbench & Scoreboard Engineer
# ============================================================================
from .gemini_client import call_agent_llm, extract_code

class TBEngineerAgent:
    SYSTEM_INSTRUCTION = """
    You are a Verification Testbench Engineer.
    Responsibilities:
    - Develop self-checking testbenches with Bus Functional Models (BFM tasks: apb_write, apb_read).
    - Implement Scoreboard comparison tracking transmitted vs received packets.
    - Provide precise timing and clock generators.
    - Output Verilog code within ```verilog ``` markdown tags.
    """

    def generate_tb(self, top_module: str, spec: str, vplan: str) -> str:
        prompt = f"Write self-checking Verilog testbench for '{top_module}' fulfilling this vPlan:\n{vplan}\nSpec:\n{spec}"
        raw = call_agent_llm(prompt, self.SYSTEM_INSTRUCTION)
        return extract_code(raw, "verilog")
