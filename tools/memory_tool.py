# tools/memory_tool.py
from crewai.tools import BaseTool
from utils.memory_manager import MemoryManager

class MemoryTool(BaseTool):
    name: str = "Series Memory Tool"
    description: str = "Use this tool to query the memory of past episodes to ensure story continuity. Input should be a question about past events."
    memory_manager: MemoryManager

    def _run(self, query: str) -> str:
        return self.memory_manager.get_relevant_context(query)