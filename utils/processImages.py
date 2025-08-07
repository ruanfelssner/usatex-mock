import os
from PIL import Image

def process_images(input_folder):
    # Pastas de saída
    thumb_folder = os.path.join(input_folder, "../static/assets/thumb")
    modelos_folder = os.path.join(input_folder, "../static/assets/modelos")

    # Criar as pastas de saída, se não existirem
    os.makedirs(thumb_folder, exist_ok=True)
    os.makedirs(modelos_folder, exist_ok=True)

    # Configurações de tamanho
    thumb_size = (128, 128)  # Tamanho fixo para miniaturas
    modelos_size = (1182, 1182)  # Tamanho máximo para manter a proporção

    # Iterar por todos os arquivos na pasta de entrada
    for file_name in os.listdir(input_folder):
        if file_name.lower().endswith((".jpg", ".jpeg", ".png")):
            file_path = os.path.join(input_folder, file_name)

            # Abrir a imagem
            with Image.open(file_path) as img:
                # Obter o nome base sem a extensão
                base_name = file_name.split("_")[1]

                # Criar a miniatura (exatamente 128x128)
                thumb_image = img.resize(thumb_size)  # Redimensionar para tamanho fixo
                thumb_path = os.path.join(thumb_folder, f"{base_name}")
                thumb_image.save(thumb_path, "JPEG", quality=85)
                print(f"Miniatura salva: {thumb_path}")

                # Criar o modelo redimensionado (mantendo proporção)
                modelos_image = img.copy()
                modelos_image.thumbnail(modelos_size)
                modelos_path = os.path.join(modelos_folder, f"{base_name}")
                modelos_image.save(modelos_path, "JPEG", quality=85)
                print(f"Imagem redimensionada salva: {modelos_path}")

if __name__ == "__main__":
    # Pasta de entrada onde as imagens estão localizadas
    input_folder = "./base-images"  # Mesma pasta do script
    process_images(input_folder)
