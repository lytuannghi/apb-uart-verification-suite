# ============================================================================
# Agent 2: DV Lead & Verification Planner
# ============================================================================
from .gemini_client import call_agent_llm

class DVPlannerAgent:
    SYSTEM_INSTRUCTION = """
    You are a Lead Design Verification (DV) Engineer.
    Your responsibility:
    - Analyze architectural specifications to extract a comprehensive Verification Plan (vPlan).
    - Map every hardware feature to individual test cases and expected assertions.
    - Identify subtle corner cases: FIFO overflow, FIFO underflow, simultaneous read/write, asynchronous reset asserting during active transmission, and bus protocol illegal handshakes.
    """

    def generate_vplan(self, spec_text: str) -> str:
        prompt = f"Develop a comprehensive, industry-grade Verification Plan (vPlan) based on this architecture:\n{spec_text}"
        return call_agent_llm(prompt, self.SYSTEM_INSTRUCTION)
