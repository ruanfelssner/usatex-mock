#!/usr/bin/env python3
"""
Script Principal para Processamento de Imagens UsaTex
Executa todo o pipeline de processamento de imagens:
1. Limpa pastas de destino
2. Padroniza nomes dos arquivos
3. Gera thumbs
4. Gera JSONs de metadata
5. Atualiza mockups se necessário
"""

import os
import re
import shutil
import json
import subprocess
import sys
from PIL import Image
from pathlib import Path

class ImageProcessor:
    def __init__(self):
        self.base_folder = "./base-images"
        self.thumb_folder = "./static/assets/thumb"
        self.modelos_folder = "./static/assets/modelos"
        self.mockups_folder = "./static/assets/mockups"
        
        # Configurações de tamanho
        self.thumb_size = (128, 128)
        self.modelos_size = (1182, 1182)
        
        # Estatísticas
        self.stats = {
            'renamed': 0,
            'thumbs_created': 0,
            'modelos_created': 0,
            'errors': 0
        }

    def clean_folders(self):
        """Limpa as pastas de thumb e modelos"""
        print("🧹 Limpando pastas de destino...")
        
        folders_to_clean = [self.thumb_folder, self.modelos_folder]
        
        for folder in folders_to_clean:
            if os.path.exists(folder):
                shutil.rmtree(folder)
                print(f"  ✓ Pasta {folder} limpa")
            os.makedirs(folder, exist_ok=True)
            print(f"  ✓ Pasta {folder} criada")

    def standardize_filename(self, filename):
        """
        Padroniza nomes de arquivos conforme as regras:
        - UC_202520 v1.jpg -> UC_202520-v1.jpg
        - UT4606 (2).jpg -> UT4606-2.jpg
        - UT4603V2.jpg -> UT4603-V2.jpg
        - Remove espaços extras e caracteres especiais
        """
        name, ext = os.path.splitext(filename)
        
        # Converter para lowercase a extensão
        ext = ext.lower()
        
        # Padrão 1: "UC_202520 v1" -> "UC_202520-v1"
        name = re.sub(r'\s+v(\d+)', r'-v\1', name, flags=re.IGNORECASE)
        
        # Padrão 2: "UT4606 (2)" -> "UT4606-2"
        name = re.sub(r'\s*\((\d+)\)', r'-\1', name)
        
        # Padrão 3: "UT4603V2" -> "UT4603-V2" (se não tem hífen antes do V)
        name = re.sub(r'([0-9])V([0-9])', r'\1-V\2', name)
        
        # Padrão 4: Remover espaços extras e substituir por hífen
        name = re.sub(r'\s+', '-', name.strip())
        
        # Padrão 5: Remover caracteres especiais exceto hífen e underscore
        name = re.sub(r'[^\w\-_]', '', name)
        
        # Padrão 6: Remover hífens múltiplos
        name = re.sub(r'-+', '-', name)
        
        # Padrão 7: Remover hífen no final
        name = name.rstrip('-')
        
        return f"{name}{ext}"

    def rename_files(self):
        """Renomeia arquivos na pasta base-images para padronizar"""
        print("📝 Padronizando nomes dos arquivos...")
        
        if not os.path.exists(self.base_folder):
            print(f"  ❌ Pasta {self.base_folder} não encontrada!")
            return
        
        renamed_files = []
        
        for filename in os.listdir(self.base_folder):
            if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
                old_path = os.path.join(self.base_folder, filename)
                new_filename = self.standardize_filename(filename)
                new_path = os.path.join(self.base_folder, new_filename)
                
                if filename != new_filename:
                    try:
                        # Verificar se o novo nome já existe
                        if os.path.exists(new_path):
                            print(f"  ⚠️  Arquivo {new_filename} já existe, pulando {filename}")
                            continue
                            
                        os.rename(old_path, new_path)
                        renamed_files.append((filename, new_filename))
                        self.stats['renamed'] += 1
                        print(f"  ✓ {filename} → {new_filename}")
                    except Exception as e:
                        print(f"  ❌ Erro ao renomear {filename}: {e}")
                        self.stats['errors'] += 1
        
        if not renamed_files:
            print("  ✓ Todos os arquivos já estão padronizados")
        
        return renamed_files

    def process_images(self):
        """Processa as imagens gerando thumbs e modelos redimensionados"""
        print("🖼️  Processando imagens...")
        
        if not os.path.exists(self.base_folder):
            print(f"  ❌ Pasta {self.base_folder} não encontrada!")
            return
        
        image_files = [f for f in os.listdir(self.base_folder) 
                      if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp'))]
        
        total_files = len(image_files)
        print(f"  📊 Encontradas {total_files} imagens para processar")
        
        for i, filename in enumerate(image_files, 1):
            try:
                file_path = os.path.join(self.base_folder, filename)
                
                # Extrair nome base (remover prefixo UC_ ou UT se presente)
                base_name = filename
                if filename.startswith(('UC_', 'UT')):
                    # Remove o prefixo e mantém o resto
                    base_name = filename.split('_', 1)[1] if '_' in filename else filename[2:]
                
                print(f"  [{i:3d}/{total_files}] Processando: {filename}")
                
                with Image.open(file_path) as img:
                    # Converter para RGB se necessário (para JPEGs)
                    if img.mode in ('RGBA', 'LA', 'P'):
                        img = img.convert('RGB')
                    
                    # Criar thumbnail (128x128 exato)
                    thumb_image = img.copy()
                    thumb_image.thumbnail(self.thumb_size, Image.Resampling.LANCZOS)
                    
                    # Centralizar a imagem em um canvas 128x128
                    thumb_canvas = Image.new('RGB', self.thumb_size, (255, 255, 255))
                    offset = ((self.thumb_size[0] - thumb_image.width) // 2,
                             (self.thumb_size[1] - thumb_image.height) // 2)
                    thumb_canvas.paste(thumb_image, offset)
                    
                    thumb_path = os.path.join(self.thumb_folder, base_name)
                    thumb_canvas.save(thumb_path, "JPEG", quality=85, optimize=True)
                    self.stats['thumbs_created'] += 1
                    
                    # Criar modelo redimensionado (mantendo proporção)
                    modelos_image = img.copy()
                    modelos_image.thumbnail(self.modelos_size, Image.Resampling.LANCZOS)
                    modelos_path = os.path.join(self.modelos_folder, base_name)
                    modelos_image.save(modelos_path, "JPEG", quality=90, optimize=True)
                    self.stats['modelos_created'] += 1
                    
            except Exception as e:
                print(f"    ❌ Erro ao processar {filename}: {e}")
                self.stats['errors'] += 1

    def generate_images_json(self):
        """Gera o JSON com a lista de imagens (equivalente ao listaImages.py)"""
        print("📄 Gerando listaImages.json...")
        
        try:
            image_files = []
            if os.path.exists(self.thumb_folder):
                image_files = [f for f in os.listdir(self.thumb_folder) 
                              if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp'))]
                image_files.sort()  # Ordenar alfabeticamente
            
            # Criar o JSON
            data = {'imagens': image_files}
            
            with open('./listaImages.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"  ✓ listaImages.json criado com {len(image_files)} imagens")
            
        except Exception as e:
            print(f"  ❌ Erro ao gerar listaImages.json: {e}")
            self.stats['errors'] += 1

    def generate_mockups_json(self):
        """Executa o script generateMockupsJson.py se houver novos mockups"""
        print("🎭 Verificando mockups...")
        
        try:
            # Verificar se há arquivos de mockup
            if os.path.exists(self.mockups_folder):
                mockup_files = [f for f in os.listdir(self.mockups_folder) 
                               if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg'))]
                
                if mockup_files:
                    # Executar o script de mockups
                    result = subprocess.run([sys.executable, 'generateMockupsJson.py'], 
                                          capture_output=True, text=True)
                    
                    if result.returncode == 0:
                        print(f"  ✓ {result.stdout.strip()}")
                    else:
                        print(f"  ❌ Erro ao gerar mockups JSON: {result.stderr}")
                        self.stats['errors'] += 1
                else:
                    print("  ℹ️  Nenhum arquivo de mockup encontrado")
            else:
                print("  ℹ️  Pasta de mockups não existe")
                
        except Exception as e:
            print(f"  ❌ Erro ao processar mockups: {e}")
            self.stats['errors'] += 1

    def print_statistics(self):
        """Imprime estatísticas do processamento"""
        print("\n" + "="*60)
        print("📊 RELATÓRIO DE PROCESSAMENTO")
        print("="*60)
        print(f"Arquivos renomeados:     {self.stats['renamed']}")
        print(f"Thumbnails criados:      {self.stats['thumbs_created']}")
        print(f"Modelos criados:         {self.stats['modelos_created']}")
        print(f"Erros encontrados:       {self.stats['errors']}")
        print("="*60)
        
        if self.stats['errors'] == 0:
            print("✅ Processamento concluído com sucesso!")
        else:
            print(f"⚠️  Processamento concluído com {self.stats['errors']} erro(s)")

    def run(self):
        """Executa todo o pipeline de processamento"""
        print("🚀 INICIANDO PROCESSAMENTO DE IMAGENS USATEX")
        print("="*60)
        
        try:
            # 1. Limpar pastas de destino
            self.clean_folders()
            print()
            
            # 2. Padronizar nomes dos arquivos
            self.rename_files()
            print()
            
            # 3. Processar imagens (gerar thumbs e modelos)
            self.process_images()
            print()
            
            # 4. Gerar JSON das imagens
            self.generate_images_json()
            print()
            
            # 5. Gerar JSON dos mockups se necessário
            self.generate_mockups_json()
            
            # 6. Mostrar estatísticas
            self.print_statistics()
            
        except KeyboardInterrupt:
            print("\n\n⛔ Processamento interrompido pelo usuário")
        except Exception as e:
            print(f"\n\n❌ Erro crítico: {e}")
            self.stats['errors'] += 1

def main():
    """Função principal"""
    processor = ImageProcessor()
    processor.run()

if __name__ == "__main__":
    main()
