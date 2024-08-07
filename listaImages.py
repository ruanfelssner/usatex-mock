import os
import json

# Lista para armazenar os nomes das imagens
nomes_das_imagens = []
caminho_da_pasta = './static/assets/thumb'

# Percorre os arquivos na pasta
for nome_do_arquivo in os.listdir(caminho_da_pasta):
    # Adiciona o nome do arquivo à lista
    nomes_das_imagens.append(nome_do_arquivo)

# Cria um dicionário com a lista de nomes das imagens
dados_json = {'imagens': nomes_das_imagens}

# Converte o dicionário para formato JSON
json_resultante = json.dumps(dados_json, indent=2)

# Salva o JSON em um arquivo
caminho_do_arquivo_json = './listaImages.json'
with open(caminho_do_arquivo_json, 'w') as arquivo_json:
    arquivo_json.write(json_resultante)

print(f'JSON criado com sucesso em {caminho_do_arquivo_json}')