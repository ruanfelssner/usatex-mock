#!/usr/bin/env python3
"""
Utilitários Adicionais para Processamento de Imagens
Inclui funções específicas para casos especiais
"""

import os
import re
import shutil
from pathlib import Path

class ImageUtils:
    def __init__(self):
        self.base_folder = "./base-images"
    
    def preview_name_changes(self):
        """Preview das mudanças de nomes sem executar"""
        print("🔍 PREVIEW DAS MUDANÇAS DE NOMES")
        print("="*60)
        
        if not os.path.exists(self.base_folder):
            print(f"❌ Pasta {self.base_folder} não encontrada!")
            return
        
        changes = []
        for filename in sorted(os.listdir(self.base_folder)):
            if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
                new_name = self.standardize_filename(filename)
                if filename != new_name:
                    changes.append((filename, new_name))
        
        if changes:
            print(f"📊 {len(changes)} arquivos serão renomeados:")
            print()
            for old, new in changes:
                print(f"  {old}")
                print(f"  → {new}")
                print()
        else:
            print("✅ Todos os arquivos já estão com nomes padronizados")
    
    def standardize_filename(self, filename):
        """Mesma função de padronização do script principal"""
        name, ext = os.path.splitext(filename)
        ext = ext.lower()
        
        # Padrões de normalização
        name = re.sub(r'\s+v(\d+)', r'-v\1', name, flags=re.IGNORECASE)
        name = re.sub(r'\s*\((\d+)\)', r'-\1', name)
        name = re.sub(r'([0-9])V([0-9])', r'\1-V\2', name)
        name = re.sub(r'\s+', '-', name.strip())
        name = re.sub(r'[^\w\-_]', '', name)
        name = re.sub(r'-+', '-', name)
        name = name.rstrip('-')
        
        return f"{name}{ext}"
    
    def find_duplicates(self):
        """Encontra possíveis duplicatas baseado nos nomes"""
        print("🔍 VERIFICANDO DUPLICATAS")
        print("="*60)
        
        if not os.path.exists(self.base_folder):
            print(f"❌ Pasta {self.base_folder} não encontrada!")
            return
        
        # Agrupar por nome base
        groups = {}
        for filename in os.listdir(self.base_folder):
            if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
                # Extrair número base
                base_match = re.search(r'(UC_\d+|UT\d+)', filename)
                if base_match:
                    base = base_match.group(1)
                    if base not in groups:
                        groups[base] = []
                    groups[base].append(filename)
        
        # Encontrar grupos com múltiplos arquivos
        duplicates = {k: v for k, v in groups.items() if len(v) > 1}
        
        if duplicates:
            print(f"📊 Encontrados {len(duplicates)} grupos com variações:")
            print()
            for base, files in duplicates.items():
                print(f"  {base}:")
                for file in sorted(files):
                    print(f"    - {file}")
                print()
        else:
            print("✅ Nenhuma duplicata encontrada")
    
    def validate_images(self):
        """Valida se todas as imagens podem ser abertas"""
        print("🔍 VALIDANDO IMAGENS")
        print("="*60)
        
        try:
            from PIL import Image
        except ImportError:
            print("❌ PIL/Pillow não está instalado. Execute: pip install pillow")
            return
        
        if not os.path.exists(self.base_folder):
            print(f"❌ Pasta {self.base_folder} não encontrada!")
            return
        
        corrupted = []
        valid = 0
        
        for filename in os.listdir(self.base_folder):
            if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
                file_path = os.path.join(self.base_folder, filename)
                try:
                    with Image.open(file_path) as img:
                        img.verify()  # Verificar se a imagem é válida
                    valid += 1
                    print(f"  ✅ {filename}")
                except Exception as e:
                    corrupted.append((filename, str(e)))
                    print(f"  ❌ {filename}: {e}")
        
        print()
        print(f"📊 Resultado: {valid} válidas, {len(corrupted)} corrompidas")
        
        if corrupted:
            print("\n⚠️  Imagens corrompidas encontradas:")
            for filename, error in corrupted:
                print(f"  - {filename}: {error}")
    
    def clean_temp_files(self):
        """Remove arquivos temporários e backups"""
        print("🧹 LIMPANDO ARQUIVOS TEMPORÁRIOS")
        print("="*60)
        
        patterns = ['*.tmp', '*.bak', '*~', 'Thumbs.db', '.DS_Store']
        removed = 0
        
        for pattern in patterns:
            for file_path in Path(self.base_folder).glob(pattern):
                try:
                    file_path.unlink()
                    print(f"  ✅ Removido: {file_path.name}")
                    removed += 1
                except Exception as e:
                    print(f"  ❌ Erro ao remover {file_path.name}: {e}")
        
        if removed == 0:
            print("  ✅ Nenhum arquivo temporário encontrado")
        else:
            print(f"\n📊 {removed} arquivo(s) temporário(s) removido(s)")

def main():
    import sys
    
    utils = ImageUtils()
    
    if len(sys.argv) < 2:
        print("🛠️  UTILITÁRIOS DE IMAGEM USATEX")
        print("="*60)
        print("Uso: python image_utils.py <comando>")
        print()
        print("Comandos disponíveis:")
        print("  preview    - Visualizar mudanças de nomes")
        print("  duplicates - Encontrar possíveis duplicatas")
        print("  validate   - Validar integridade das imagens")
        print("  clean      - Limpar arquivos temporários")
        print()
        print("Exemplo: python image_utils.py preview")
        return
    
    command = sys.argv[1].lower()
    
    if command == 'preview':
        utils.preview_name_changes()
    elif command == 'duplicates':
        utils.find_duplicates()
    elif command == 'validate':
        utils.validate_images()
    elif command == 'clean':
        utils.clean_temp_files()
    else:
        print(f"❌ Comando '{command}' não reconhecido")
        print("Use: preview, duplicates, validate, ou clean")

if __name__ == "__main__":
    main()
