import os
import json
from pathlib import Path

def generate_mockups_json():
    """
    Gera um arquivo JSON com a lista de mockups baseado nas imagens
    encontradas na pasta static/assets/mockups
    """
    
    # Caminho para a pasta de mockups
    mockups_path = Path("static/assets/mockups")
    
    # Verificar se a pasta existe
    if not mockups_path.exists():
        print(f"Erro: Pasta {mockups_path} não encontrada!")
        return
    
    # Extensões de imagem suportadas
    image_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg'}
    
    # Lista para armazenar os mockups
    mockups_list = []
    
    # Percorrer todos os arquivos na pasta
    for file in sorted(mockups_path.iterdir()):
        if file.is_file() and file.suffix.lower() in image_extensions:
            # Nome do arquivo sem extensão
            name = file.stem
            
            # Caminho da imagem (relativo ao projeto)
            img_path = f"/assets/mockups/{file.name}"
            
            # Adicionar à lista
            mockups_list.append({
                "name": name,
                "img": img_path
            })
    
    # Criar o objeto JSON final
    mockups_data = {
        "mockups": mockups_list
    }
    
    # Salvar o arquivo JSON
    output_file = "listaMockups.json"
    
    # Verificar se o arquivo já existe e se houve mudanças
    file_changed = True
    if Path(output_file).exists():
        try:
            with open(output_file, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
            file_changed = existing_data != mockups_data
        except:
            file_changed = True
    
    if file_changed:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(mockups_data, f, indent=2, ensure_ascii=False)
        
        print(f"Arquivo {output_file} criado/atualizado com sucesso!")
        print(f"Total de mockups encontrados: {len(mockups_list)}")
        
        # Mostrar alguns exemplos
        print("\nPrimeiros 5 mockups:")
        for mockup in mockups_list[:5]:
            print(f"  - {mockup['name']}: {mockup['img']}")
        
        if len(mockups_list) > 5:
            print(f"  ... e mais {len(mockups_list) - 5} mockups")
    else:
        print(f"Nenhuma mudança detectada. O arquivo {output_file} está atualizado.")
    
    return mockups_list

def watch_folder():
    """
    Função para observar mudanças na pasta de mockups
    (requer instalação do watchdog: pip install watchdog)
    """
    try:
        from watchdog.observers import Observer
        from watchdog.events import FileSystemEventHandler
        import time
        
        class MockupHandler(FileSystemEventHandler):
            def on_any_event(self, event):
                if not event.is_directory:
                    print(f"Mudança detectada: {event.event_type} - {event.src_path}")
                    generate_mockups_json()
        
        event_handler = MockupHandler()
        observer = Observer()
        observer.schedule(event_handler, "static/assets/mockups", recursive=False)
        observer.start()
        
        print("Observando mudanças na pasta de mockups... (Ctrl+C para parar)")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
        
    except ImportError:
        print("Para observar mudanças automaticamente, instale o watchdog:")
        print("pip install watchdog")
        print("Depois execute: python generateMockupsJson.py --watch")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--watch":
        watch_folder()
    else:
        generate_mockups_json()
