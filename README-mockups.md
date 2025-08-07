# Gerador de JSON para Mockups

Este script Python automatiza a criação de um arquivo JSON com a lista de mockups baseado nas imagens encontradas na pasta `static/assets/mockups`.

## Como usar

### Uso básico

```bash
python generateMockupsJson.py
```

Este comando irá:

1. Ler todas as imagens da pasta `static/assets/mockups`
2. Gerar um arquivo `listaMockups.json` com a estrutura necessária
3. O arquivo `Model.vue` automaticamente usará este JSON

### Observar mudanças (opcional)

Para observar automaticamente mudanças na pasta de mockups:

1. Instale a dependência:

```bash
pip install watchdog
```

2. Execute o modo watch:

```bash
python generateMockupsJson.py --watch
```

## Estrutura do JSON gerado

```json
{
  "mockups": [
    {
      "name": "nome-do-arquivo",
      "img": "/assets/mockups/nome-do-arquivo.png"
    }
  ]
}
```

## Formatos suportados

- PNG
- JPG/JPEG
- GIF
- WEBP
- SVG

## Integração com Model.vue

O arquivo `Model.vue` foi modificado para importar automaticamente o JSON:

```javascript
import listaMockups from "@/listaMockups.json";

// No data():
listMockups: listaMockups.mockups;
```

## Benefícios

1. **Automático**: Não precisa mais editar manualmente a lista no código
2. **Sincronizado**: Sempre reflete as imagens realmente disponíveis
3. **Manutenção fácil**: Basta adicionar/remover imagens da pasta
4. **Consistente**: Nomes baseados nos arquivos reais
