import torch
from safetensors.torch import save_file

print("🔄 Convirtiendo pytorch_model.bin a safetensors...")

model_dir = "/home/honores/.local/share/instructlab/checkpoints/hf_format/samples_0"
bin_file = f"{model_dir}/pytorch_model.bin"
safetensors_file = f"{model_dir}/model.safetensors"

# Cargar el modelo PyTorch
print("📦 Cargando pytorch_model.bin...")
state_dict = torch.load(bin_file, map_location="cpu")

# Guardar en formato safetensors
print("💾 Guardando como model.safetensors...")
save_file(state_dict, safetensors_file)

print(f"✅ Conversión completa: {safetensors_file}")
