# models/svd_model.py
import torch
from diffusers import StableVideoDiffusionPipeline
from diffusers.utils import load_image, export_to_video
from PIL import Image
import gc

class SVDGenerator:
    _instance = None
    pipe = None
    device = "cpu"

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(SVDGenerator, cls).__new__(cls)
            
            print(" SVD: Initializing LIGHTER Stable Video Diffusion Pipeline...")
            # --- MODEL CHANGE IS HERE ---
            # We are now using the smaller, less memory-intensive SVD model.
            cls.pipe = StableVideoDiffusionPipeline.from_pretrained(
                "stabilityai/stable-video-diffusion-img2vid", # The non-'xt' version
                torch_dtype=torch.float16, 
                variant="fp16"
            )
            
            # Determine the device and configure it
            if torch.cuda.is_available():
                print(" SVD: CUDA (NVIDIA GPU) detected. Enabling offload.")
                cls.device = "cuda"
                # For CUDA, offloading is still the best strategy
                cls.pipe.enable_model_cpu_offload()
            elif torch.backends.mps.is_available():
                print(" SVD: MPS (Apple Silicon GPU) detected. Moving pipe to MPS.")
                cls.device = "mps"
                # On Mac, we will try moving the whole pipe to the GPU.
                # This lighter model should fit in memory.
                cls.pipe.to(cls.device)
            else:
                print("⚠️ WARNING: No compatible GPU detected. SVD will run on CPU only.")
                cls.device = "cpu"
                cls.pipe.to(cls.device)

        return cls._instance

    def generate(self, image_path: str, output_path: str):
        # Ensure the pipe is on the correct device before running
        self.pipe.to(self.device)

        try:
            print(f" SVD: Loading initial image from {image_path}")
            image = load_image(image_path)
            # This smaller model was trained on 256x256 images, but can be adapted.
            # We'll still use our target aspect ratio.
            image = image.resize((1024, 576))

            generator = torch.manual_seed(42)
            
            print(" SVD: Generating video frames with LIGHTER model...")
            # This model generates fewer frames by default (14 instead of 25)
            frames = self.pipe(image, decode_chunk_size=8, generator=generator).frames[0]
            
            print(f" SVD: Exporting video to {output_path}")
            # Generating at a slightly higher FPS as the clips are shorter
            export_to_video(frames, output_path, fps=10)
            
            return f"Successfully generated SVD video at {output_path}"
        
        except Exception as e:
            return f"Error during SVD video generation on device '{self.device}': {e}"
        
        finally:
            print(" SVD: Cleaning up accelerator memory...")
            # On CUDA, it's good practice to move back to CPU after offloading.
            if self.device == "cuda":
                self.pipe.to("cpu")
                torch.cuda.empty_cache()
            gc.collect()


# This allows the script to be run directly for testing
if __name__ == '__main__':
    dummy_image = Image.new('RGB', (1024, 576), color = 'red')
    dummy_image_path = "dummy_start_frame.png"
    dummy_image.save(dummy_image_path)

    print("--- Running SVD Test with LIGHTER model ---")
    svd_gen = SVDGenerator()
    result = svd_gen.generate(dummy_image_path, "test_output.mp4")
    print(f"--- Test Result: {result} ---")