# tools/memory_tool.py
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from utils.memory_manager import MemoryManager





# tools/memory_tool.py
from crewai.tools import BaseTool
from utils.memory_manager import MemoryManager

class MemoryTool(BaseTool):
    name: str = "Series Memory Tool"
    description: str = "Use this tool to query the memory of past episodes to ensure story continuity. Input should be a question about past events."
    memory_manager: MemoryManager

    def _run(self, query: str) -> str:
        return self.memory_manager.get_relevant_context(query)
    


class MemoryReaderToolSchema(BaseModel):
    """Input schema for MemoryReaderTool."""
    query: str = Field(..., description="The question to ask the long-term memory about past episodes.")

class MemoryReaderTool(BaseTool):
    name: str = "Series Memory Reader"
    description: str = "Use this to READ the memory of past episodes to ensure story continuity. Input should be a question about past events."
    args_schema: type[BaseModel] = MemoryReaderToolSchema
    # Define memory_manager as a class attribute. Pydantic will handle it.
    memory_manager: MemoryManager

    def _run(self, query: str) -> str:
        return self.memory_manager.get_relevant_context(query)


# --- CORRECT SCHEMA AND TOOL FOR WRITING MEMORY ---
class MemoryWriterToolSchema(BaseModel):
    """Input schema for MemoryWriterTool."""
    episode_id: int = Field(..., description="The ID number of the episode being summarized.")
    summary: str = Field(..., description="The concise summary of the episode's plot to be saved.")

class MemoryWriterTool(BaseTool):
    name: str = "Series Memory Writer"
    description: str = "Use this to WRITE a summary of the current episode to the long-term memory. This ensures future episodes can build upon it."
    args_schema: type[BaseModel] = MemoryWriterToolSchema
    # Define memory_manager as a class attribute. Pydantic will handle it.
    memory_manager: MemoryManager

    def _run(self, episode_id: int, summary: str) -> str:
        self.memory_manager.add_episode_summary(episode_id, summary)
        return f"Successfully saved summary for Episode {episode_id} to memory."