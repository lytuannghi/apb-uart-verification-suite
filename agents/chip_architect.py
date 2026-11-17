# ============================================================================
# Agent 1: Chip Architect
# ============================================================================
from .gemini_client import call_agent_llm

class ChipArchitectAgent:
    SYSTEM_INSTRUCTION = """
    You are an expert Principal Chip Architect specialized in AMBA Bus systems (APB, AXI, AHB) and IP core specifications.
    Your responsibility:
    - Define hardware architecture, clock domains, and reset strategies.
    - Specify full Register Map with byte offsets, access permissions (RO, RW, WO), and bitfield descriptions.
    - Formulate standard bus timing requirements and handshakes.
    """

    def generate_spec(self, requirements: str) -> str:
        prompt = f"Define complete architectural specification for:\n{requirements}"
        return call_agent_llm(prompt, self.SYSTEM_INSTRUCTION)
