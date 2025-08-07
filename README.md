# UsaTex - Sistema de Atualização

Sistema unificado para processamento de imagens e metadados do projeto UsaTex.

## 🚀 Uso Rápido

### Processamento Completo (Recomendado)

```bash
python update.py
```

### Menu Interativo (Windows)

```cmd
processar_imagens.bat
```

## 📋 Comandos Disponíveis

```bash
python update.py                 # Processamento completo
python update.py --preview       # Ver mudanças antes de executar
python update.py --clean         # Apenas limpeza de pastas
python update.py --validate      # Apenas validação de imagens
python update.py --duplicates    # Buscar duplicatas
python update.py --mockups       # Apenas atualizar mockups
python update.py --help          # Ajuda completa
```

## 📁 Estrutura

```
projeto/
├── base-images/              # 📂 Imagens originais
├── static/assets/
│   ├── thumb/               # 📂 Thumbnails 128x128 (gerado)
│   ├── modelos/             # 📂 Imagens redimensionadas (gerado)
│   └── mockups/             # 📂 Mockups
├── update.py                # 🎯 Script principal
├── processar_imagens.bat    # 📝 Menu interativo
├── listaImages.json         # 📄 Metadados (gerado)
├── listaMockups.json        # 📄 Mockups (gerado)
└── utils/                   # 📂 Scripts antigos (backup)
```

## 🔧 Funcionalidades

### ✅ Padronização Automática

- `UC_202520 v1.jpg` → `UC_202520-v1.jpg`
- `UT4606 (2).jpg` → `UT4606-2.jpg`
- `UT4603V2.jpg` → `UT4603-V2.jpg`

### ✅ Processamento de Imagens

- **Thumbnails**: 128x128px (centralizado)
- **Modelos**: Até 1182x1182px (mantém proporção)
- **Qualidade**: JPEG otimizado (85%/90%)

### ✅ Validação e Análise

- Verifica integridade das imagens
- Detecta duplicatas/variações
- Preview antes da execução

### ✅ Geração de Metadados

- `listaImages.json` - Lista de todas as imagens
- `listaMockups.json` - Lista de mockups disponíveis

## 📦 Pré-requisitos

```bash
pip install pillow
```

## 🔄 Fluxo de Trabalho

1. **Adicione imagens** na pasta `base-images/`
2. **Execute**: `python update.py`
3. **Verifique** as pastas `thumb/` e `modelos/`
4. **Teste** a aplicação Vue.js

---

## Build Setup da Aplicação Vue.js

```bash
# install dependencies
$ yarn install

# serve with hot reload at localhost:3000
$ yarn dev

# build for production and launch server
$ yarn build
$ yarn start

# generate static project
$ yarn generate
```

For detailed explanation on how things work, check out the [documentation](https://nuxtjs.org).

## Special Directories

You can create the following extra directories, some of which have special behaviors. Only `pages` is required; you can delete them if you don't want to use their functionality.

### `assets`

The assets directory contains your uncompiled assets such as Stylus or Sass files, images, or fonts.

More information about the usage of this directory in [the documentation](https://nuxtjs.org/docs/2.x/directory-structure/assets).

### `components`

The components directory contains your Vue.js components. Components make up the different parts of your page and can be reused and imported into your pages, layouts and even other components.

More information about the usage of this directory in [the documentation](https://nuxtjs.org/docs/2.x/directory-structure/components).

### `layouts`

Layouts are a great help when you want to change the look and feel of your Nuxt app, whether you want to include a sidebar or have distinct layouts for mobile and desktop.

More information about the usage of this directory in [the documentation](https://nuxtjs.org/docs/2.x/directory-structure/layouts).

### `pages`

This directory contains your application views and routes. Nuxt will read all the `*.vue` files inside this directory and setup Vue Router automatically.

More information about the usage of this directory in [the documentation](https://nuxtjs.org/docs/2.x/get-started/routing).

### `plugins`

The plugins directory contains JavaScript plugins that you want to run before instantiating the root Vue.js Application. This is the place to add Vue plugins and to inject functions or constants. Every time you need to use `Vue.use()`, you should create a file in `plugins/` and add its path to plugins in `nuxt.config.js`.

More information about the usage of this directory in [the documentation](https://nuxtjs.org/docs/2.x/directory-structure/plugins).

### `static`

This directory contains your static files. Each file inside this directory is mapped to `/`.

Example: `/static/robots.txt` is mapped as `/robots.txt`.

More information about the usage of this directory in [the documentation](https://nuxtjs.org/docs/2.x/directory-structure/static).

### `store`

This directory contains your Vuex store files. Creating a file in this directory automatically activates Vuex.

More information about the usage of this directory in [the documentation](https://nuxtjs.org/docs/2.x/directory-structure/store).
