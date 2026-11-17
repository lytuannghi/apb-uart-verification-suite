# ============================================================================
# Agent 5: Assertion & Corner-Case Specialist
# ============================================================================
from .gemini_client import call_agent_llm

class AssertionSpecialistAgent:
    SYSTEM_INSTRUCTION = """
    You are a Formal Verification and Assertion-Based Verification (ABV) Specialist.
    Responsibilities:
    - Formulate protocol checkers (e.g., PENABLE must assert exactly one cycle after PSEL).
    - Identify subtle boundary conditions and corner-case scenarios (FIFO depth + 1 writes, reads on empty, back-to-back bus accesses).
    - Provide actionable feedback to the Testbench and RTL agents to achieve 100% functional coverage.
    """

    def analyze_coverage_and_corner_cases(self, vplan: str, sim_log: str) -> str:
        prompt = f"Analyze simulation log against vPlan to identify missed corner cases or protocol risks:\nvPlan:\n{vplan}\nLog:\n{sim_log}"
        return call_agent_llm(prompt, self.SYSTEM_INSTRUCTION)
