# tools/local_image_tool.py
import os
import torch
from diffusers import DiffusionPipeline
from crewai.tools import BaseTool
from pydantic import BaseModel, Field, PrivateAttr
from typing import Any # Import Any

class LocalImageGeneratorToolSchema(BaseModel):
    prompt: str = Field(..., description="A detailed, descriptive prompt for the image.")
    file_path: str = Field(..., description="The local path to save the generated image.")

class LocalImageGeneratorTool(BaseTool):
    name: str = "Local Image Generator"
    description: str = "Generates a still image using a local Stable Diffusion model."
    args_schema: type[BaseModel] = LocalImageGeneratorToolSchema
    
    # 1. Define the attributes at the class level
    _pipeline: Any = PrivateAttr()
    _device: str = PrivateAttr()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not torch.backends.mps.is_available():
            print("Warning: MPS not available. This tool is optimized for Apple Silicon. It will run on CPU, but may be very slow.")
            self._device = "cpu"
        else:
            self._device = "mps"
        
        print("🚀 Initializing local Stable Diffusion pipeline...")
        model_id = "digiplay/AbsoluteReality_v1.8.1"
        # 2. Assign to the private attribute
        self._pipeline = DiffusionPipeline.from_pretrained(
            model_id, 
            torch_dtype=torch.float16,
            use_safetensors=True
        ).to(self._device)
        print("✅ Local Stable Diffusion pipeline loaded.")

    def _run(self, prompt: str, file_path: str) -> str:
        print(f"🎨 Generating local image with prompt: '{prompt}'")
        try:
            with torch.inference_mode():
                # 3. Use the private attribute
                image = self._pipeline(prompt, num_inference_steps=20).images[0]
            
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            image.save(file_path)
            return f"Successfully saved local image to {file_path}"
        except Exception as e:
            return f"Error during local image generation: {e}"