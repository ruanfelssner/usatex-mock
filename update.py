#!/usr/bin/env python3
"""
UsaTex - Sistema Unificado de Atualização
Gerencia todo o processamento de imagens e metadados do projeto

Uso:
    python update.py                # Processamento completo
    python update.py --preview      # Preview das mudanças
    python update.py --clean        # Apenas limpeza
    python update.py --validate     # Apenas validação
    python update.py --duplicates   # Buscar duplicatas
    python update.py --mockups      # Apenas mockups
    python update.py --help         # Ajuda
"""

import os
import re
import shutil
import json
import subprocess
import sys
import argparse
from pathlib import Path
from typing import List, Tuple, Dict

# Importar PIL apenas quando necessário
try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

class UsaTexUpdater:
    """Sistema unificado para processamento de imagens e metadados"""
    
    def __init__(self):
        self.base_folder = Path("./base-images")
        self.thumb_folder = Path("./static/assets/thumb")
        self.modelos_folder = Path("./static/assets/modelos")
        self.mockups_folder = Path("./static/assets/mockups")
        
        # Configurações
        self.thumb_size = (128, 128)
        self.modelos_size = (1182, 1182)
        self.image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg'}
        
        # Estatísticas
        self.stats = {
            'renamed': 0,
            'thumbs_created': 0,
            'modelos_created': 0,
            'errors': 0,
            'validated': 0,
            'corrupted': 0
        }
    
    def print_header(self, title: str):
        """Imprime cabeçalho formatado"""
        print("\n" + "=" * 60)
        print(f"🚀 {title}")
        print("=" * 60)
    
    def print_section(self, title: str):
        """Imprime seção formatada"""
        print(f"\n{title}")
        print("-" * len(title))
    
    def standardize_filename(self, filename: str) -> str:
        """Padroniza nomes de arquivos"""
        name, ext = os.path.splitext(filename)
        ext = ext.lower()
        
        # Aplicar regras de padronização
        patterns = [
            (r'\s+v(\d+)', r'-v\1'),           # "v1" -> "-v1"
            (r'\s*\((\d+)\)', r'-\1'),         # "(2)" -> "-2"
            (r'([0-9])V([0-9])', r'\1-V\2'),   # "V2" -> "-V2"
            (r'\s+', '-'),                      # espaços -> hífen
            (r'[^\w\-_]', ''),                 # remover especiais
            (r'-+', '-'),                       # múltiplos hífens
        ]
        
        for pattern, replacement in patterns:
            name = re.sub(pattern, replacement, name, flags=re.IGNORECASE)
        
        return f"{name.rstrip('-')}{ext}"
    
    def clean_folders(self) -> bool:
        """Limpa pastas de destino"""
        self.print_section("🧹 Limpando pastas de destino")
        
        folders = [self.thumb_folder, self.modelos_folder]
        
        for folder in folders:
            try:
                if folder.exists():
                    shutil.rmtree(folder)
                    print(f"  ✓ {folder} limpa")
                
                folder.mkdir(parents=True, exist_ok=True)
                print(f"  ✓ {folder} criada")
                
            except Exception as e:
                print(f"  ❌ Erro ao limpar {folder}: {e}")
                self.stats['errors'] += 1
                return False
        
        return True
    
    def preview_name_changes(self) -> List[Tuple[str, str]]:
        """Preview das mudanças de nomes"""
        self.print_section("🔍 Preview das mudanças de nomes")
        
        if not self.base_folder.exists():
            print(f"  ❌ Pasta {self.base_folder} não encontrada!")
            return []
        
        changes = []
        for file_path in self.base_folder.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in self.image_extensions:
                new_name = self.standardize_filename(file_path.name)
                if file_path.name != new_name:
                    changes.append((file_path.name, new_name))
        
        if changes:
            print(f"  📊 {len(changes)} arquivos serão renomeados:")
            for old, new in changes[:10]:  # Mostrar apenas os primeiros 10
                print(f"    {old} → {new}")
            if len(changes) > 10:
                print(f"    ... e mais {len(changes) - 10} arquivos")
        else:
            print("  ✅ Todos os arquivos já estão padronizados")
        
        return changes
    
    def rename_files(self) -> bool:
        """Renomeia arquivos para padronizar"""
        self.print_section("📝 Padronizando nomes dos arquivos")
        
        if not self.base_folder.exists():
            print(f"  ❌ Pasta {self.base_folder} não encontrada!")
            return False
        
        for file_path in self.base_folder.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in self.image_extensions:
                new_name = self.standardize_filename(file_path.name)
                
                if file_path.name != new_name:
                    new_path = file_path.parent / new_name
                    
                    try:
                        if new_path.exists():
                            print(f"  ⚠️  {new_name} já existe, pulando {file_path.name}")
                            continue
                        
                        file_path.rename(new_path)
                        self.stats['renamed'] += 1
                        print(f"  ✓ {file_path.name} → {new_name}")
                        
                    except Exception as e:
                        print(f"  ❌ Erro ao renomear {file_path.name}: {e}")
                        self.stats['errors'] += 1
        
        if self.stats['renamed'] == 0:
            print("  ✅ Nenhum arquivo precisou ser renomeado")
        
        return True
    
    def validate_images(self) -> bool:
        """Valida integridade das imagens"""
        self.print_section("🔍 Validando integridade das imagens")
        
        if not PIL_AVAILABLE:
            print("  ❌ PIL/Pillow não instalado. Execute: pip install pillow")
            return False
        
        if not self.base_folder.exists():
            print(f"  ❌ Pasta {self.base_folder} não encontrada!")
            return False
        
        image_files = [f for f in self.base_folder.iterdir() 
                      if f.is_file() and f.suffix.lower() in self.image_extensions]
        
        print(f"  📊 Validando {len(image_files)} imagens...")
        
        for file_path in image_files:
            try:
                with Image.open(file_path) as img:
                    img.verify()
                self.stats['validated'] += 1
            except Exception as e:
                print(f"  ❌ {file_path.name}: {e}")
                self.stats['corrupted'] += 1
        
        print(f"  ✅ {self.stats['validated']} válidas, {self.stats['corrupted']} corrompidas")
        return self.stats['corrupted'] == 0
    
    def find_duplicates(self) -> Dict[str, List[str]]:
        """Encontra possíveis duplicatas"""
        self.print_section("🔍 Verificando duplicatas")
        
        if not self.base_folder.exists():
            print(f"  ❌ Pasta {self.base_folder} não encontrada!")
            return {}
        
        groups = {}
        for file_path in self.base_folder.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in self.image_extensions:
                # Extrair número base
                base_match = re.search(r'(UC_\d+|UT\d+)', file_path.name)
                if base_match:
                    base = base_match.group(1)
                    if base not in groups:
                        groups[base] = []
                    groups[base].append(file_path.name)
        
        # Filtrar apenas grupos com múltiplos arquivos
        duplicates = {k: v for k, v in groups.items() if len(v) > 1}
        
        if duplicates:
            print(f"  📊 {len(duplicates)} grupos com variações encontrados:")
            for base, files in list(duplicates.items())[:5]:  # Mostrar apenas 5
                print(f"    {base}: {len(files)} variações")
            if len(duplicates) > 5:
                print(f"    ... e mais {len(duplicates) - 5} grupos")
        else:
            print("  ✅ Nenhuma duplicata encontrada")
        
        return duplicates
    
    def process_images(self) -> bool:
        """Processa todas as imagens"""
        self.print_section("🖼️  Processando imagens")
        
        if not PIL_AVAILABLE:
            print("  ❌ PIL/Pillow não instalado. Execute: pip install pillow")
            return False
        
        if not self.base_folder.exists():
            print(f"  ❌ Pasta {self.base_folder} não encontrada!")
            return False
        
        image_files = [f for f in self.base_folder.iterdir() 
                      if f.is_file() and f.suffix.lower() in self.image_extensions]
        
        total = len(image_files)
        print(f"  📊 Processando {total} imagens...")
        
        for i, file_path in enumerate(image_files, 1):
            try:
                # Determinar nome de saída
                output_name = file_path.name
                if file_path.name.startswith(('UC_', 'UT')):
                    parts = file_path.name.split('_', 1)
                    if len(parts) > 1:
                        output_name = parts[1]
                
                if i % 50 == 0:  # Log a cada 50 imagens
                    print(f"    [{i:3d}/{total}] Processando: {file_path.name}")
                
                with Image.open(file_path) as img:
                    # Converter para RGB se necessário
                    if img.mode in ('RGBA', 'LA', 'P'):
                        img = img.convert('RGB')
                    
                    # Criar thumbnail
                    thumb_img = img.copy()
                    thumb_img.thumbnail(self.thumb_size, Image.Resampling.LANCZOS)
                    
                    # Centralizar em canvas 128x128
                    thumb_canvas = Image.new('RGB', self.thumb_size, (255, 255, 255))
                    offset = ((self.thumb_size[0] - thumb_img.width) // 2,
                             (self.thumb_size[1] - thumb_img.height) // 2)
                    thumb_canvas.paste(thumb_img, offset)
                    
                    thumb_path = self.thumb_folder / output_name
                    thumb_canvas.save(thumb_path, "JPEG", quality=85, optimize=True)
                    self.stats['thumbs_created'] += 1
                    
                    # Criar modelo redimensionado
                    modelo_img = img.copy()
                    modelo_img.thumbnail(self.modelos_size, Image.Resampling.LANCZOS)
                    modelo_path = self.modelos_folder / output_name
                    modelo_img.save(modelo_path, "JPEG", quality=90, optimize=True)
                    self.stats['modelos_created'] += 1
                    
            except Exception as e:
                print(f"    ❌ Erro ao processar {file_path.name}: {e}")
                self.stats['errors'] += 1
        
        print(f"  ✅ Processamento concluído: {self.stats['thumbs_created']} imagens")
        return True
    
    def generate_images_json(self) -> bool:
        """Gera JSON com lista de imagens"""
        self.print_section("📄 Gerando listaImages.json")
        
        try:
            image_files = []
            if self.thumb_folder.exists():
                image_files = [f.name for f in self.thumb_folder.iterdir() 
                              if f.is_file() and f.suffix.lower() in self.image_extensions]
                image_files.sort()
            
            data = {'imagens': image_files}
            
            with open('./listaImages.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"  ✅ listaImages.json criado com {len(image_files)} imagens")
            return True
            
        except Exception as e:
            print(f"  ❌ Erro ao gerar listaImages.json: {e}")
            self.stats['errors'] += 1
            return False
    
    def update_mockups_json(self) -> bool:
        """Atualiza JSON dos mockups"""
        self.print_section("🎭 Atualizando listaMockups.json")
        
        try:
            if not self.mockups_folder.exists():
                print("  ℹ️  Pasta de mockups não existe")
                return True
            
            mockup_files = [f for f in self.mockups_folder.iterdir() 
                           if f.is_file() and f.suffix.lower() in self.image_extensions]
            
            if not mockup_files:
                print("  ℹ️  Nenhum mockup encontrado")
                return True
            
            mockups_list = []
            for file_path in sorted(mockup_files):
                mockups_list.append({
                    "name": file_path.stem,
                    "img": f"/assets/mockups/{file_path.name}"
                })
            
            data = {"mockups": mockups_list}
            
            # Verificar se houve mudanças
            output_file = Path('./listaMockups.json')
            file_changed = True
            
            if output_file.exists():
                try:
                    with open(output_file, 'r', encoding='utf-8') as f:
                        existing_data = json.load(f)
                    file_changed = existing_data != data
                except:
                    pass
            
            if file_changed:
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                print(f"  ✅ listaMockups.json atualizado com {len(mockups_list)} mockups")
            else:
                print("  ℹ️  listaMockups.json já está atualizado")
            
            return True
            
        except Exception as e:
            print(f"  ❌ Erro ao atualizar mockups: {e}")
            self.stats['errors'] += 1
            return False
    
    def print_stats(self):
        """Imprime estatísticas finais"""
        self.print_header("RELATÓRIO FINAL")
        
        print(f"📊 Arquivos renomeados:      {self.stats['renamed']}")
        print(f"🖼️  Thumbnails criados:       {self.stats['thumbs_created']}")
        print(f"📐 Modelos criados:          {self.stats['modelos_created']}")
        print(f"✅ Imagens validadas:        {self.stats['validated']}")
        print(f"💥 Imagens corrompidas:      {self.stats['corrupted']}")
        print(f"❌ Erros encontrados:        {self.stats['errors']}")
        
        print("\n" + "=" * 60)
        if self.stats['errors'] == 0:
            print("🎉 PROCESSAMENTO CONCLUÍDO COM SUCESSO!")
        else:
            print(f"⚠️  PROCESSAMENTO CONCLUÍDO COM {self.stats['errors']} ERRO(S)")
        print("=" * 60)
    
    def run_full_update(self):
        """Executa atualização completa"""
        self.print_header("USATEX - ATUALIZAÇÃO COMPLETA")
        
        steps = [
            ("Limpeza", self.clean_folders),
            ("Renomeação", self.rename_files),
            ("Processamento", self.process_images),
            ("JSON Imagens", self.generate_images_json),
            ("JSON Mockups", self.update_mockups_json),
        ]
        
        for step_name, step_func in steps:
            if not step_func():
                print(f"\n❌ Falha na etapa: {step_name}")
                return False
        
        self.print_stats()
        return True

def main():
    """Função principal com argumentos de linha de comando"""
    parser = argparse.ArgumentParser(
        description="UsaTex - Sistema Unificado de Atualização",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python update.py                 # Processamento completo
  python update.py --preview       # Ver mudanças antes de executar
  python update.py --clean         # Apenas limpeza de pastas
  python update.py --validate      # Apenas validação de imagens
  python update.py --duplicates    # Buscar duplicatas
  python update.py --mockups       # Apenas atualizar mockups
        """
    )
    
    parser.add_argument('--preview', action='store_true', 
                       help='Visualizar mudanças sem executar')
    parser.add_argument('--clean', action='store_true',
                       help='Apenas limpar pastas de destino')
    parser.add_argument('--validate', action='store_true',
                       help='Apenas validar integridade das imagens')
    parser.add_argument('--duplicates', action='store_true',
                       help='Apenas buscar duplicatas')
    parser.add_argument('--mockups', action='store_true',
                       help='Apenas atualizar JSON dos mockups')
    
    args = parser.parse_args()
    
    updater = UsaTexUpdater()
    
    try:
        # Verificar se PIL está disponível para operações que precisam
        if (not args.preview and not args.duplicates and not args.mockups) and not PIL_AVAILABLE:
            print("❌ PIL/Pillow não está instalado!")
            print("Execute: pip install pillow")
            return 1
        
        # Executar comando específico
        if args.preview:
            updater.print_header("PREVIEW DAS MUDANÇAS")
            changes = updater.preview_name_changes()
            duplicates = updater.find_duplicates()
            
        elif args.clean:
            updater.print_header("LIMPEZA DE PASTAS")
            updater.clean_folders()
            
        elif args.validate:
            updater.print_header("VALIDAÇÃO DE IMAGENS")
            updater.validate_images()
            updater.print_stats()
            
        elif args.duplicates:
            updater.print_header("BUSCA DE DUPLICATAS")
            updater.find_duplicates()
            
        elif args.mockups:
            updater.print_header("ATUALIZAÇÃO DE MOCKUPS")
            updater.update_mockups_json()
            
        else:
            # Processamento completo
            return 0 if updater.run_full_update() else 1
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\n⛔ Operação cancelada pelo usuário")
        return 1
    except Exception as e:
        print(f"\n\n❌ Erro crítico: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
