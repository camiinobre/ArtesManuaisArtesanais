# Artes Manuais Artesanais

Site estático da marca Artes Manuais (canecas, copos, camisetas, quadros, bottons, ímãs, enfeites de Natal), publicado pelo GitHub Pages a partir de `main`. O que entra em `main` vai ao ar; não há passo de deploy.

## Stack

HTML, CSS e JavaScript puros, embutidos em cada página. Não há `package.json`, build, testes, lint nem variáveis de ambiente. As únicas dependências são as fontes do Google Fonts (Baloo 2, Nunito, Caveat) e `js/qrcode.js`, que já está no repositório.

Para ver o site localmente:

```bash
python3 -m http.server 8765
```

## Páginas

- `index.html`: vitrine. As listas `canecas`, `camisetas`, `quadros`, `bottons`, `imas` e `natal` ficam no fim do `<script>`, no formato `['arquivo','Nome','Tipo',preco,'descricao']`.
- `pedido.html`: simulador de orçamento. `PRODUTOS` e `ENCOMENDA` ficam no começo do `<script>`, no formato `C("arquivo","Tipo","Nome",preco,{...})`. É a única página com tema escuro.
- `loja.html`: vitrine com sacola e Pix. `PIX`, `PRODUTOS` e `CATS` ficam no começo do `<script>`, no formato `P("arquivo","categoria","Tipo","Nome",preco,{...})`. Tem todas as categorias da vitrine, com `estoque` e `pronta` nas peças únicas.
- `calculadora.html`: calculadora interna de preços. Guarda o estado no `localStorage` do aparelho.

## Produto novo

1. Coloque duas fotos em `img/`, em retrato 4:5: `nome.webp` com 900 px de largura e `nome-sm.webp` com 480 px.
2. Acrescente o produto nos três lugares: a lista de `index.html`, `PRODUTOS` de `pedido.html` e `PRODUTOS` de `loja.html`.
3. Variação de cor não é produto novo no simulador nem na loja: entra em `fotoCor` do produto principal (ver `estrela-marrom` e `nordeste-preta`), mas tem linha própria em `index.html`.
4. O preço precisa ser o mesmo nas páginas em que aparece.

O hook `.claude/hooks/confere-produtos.py` roda depois de cada edição nessas páginas ou em `img/` e acusa produto faltando, foto faltando e preço diferente. Para rodar à mão:

```bash
python3 .claude/hooks/confere-produtos.py
```

## Estilo

- Cada página declara as próprias variáveis CSS, e os nomes não batem: `--papel` é o fundo em `index.html` e `pedido.html` e é o cartão em `calculadora.html`; `--tinta` e `--linha` têm valores diferentes. Mudança de cor precisa ser conferida página por página.
- Cores da marca: índigo `#2A0BA8`, girassol `#FCD71A`, hibisco `#7120BA`, aquarela `#AED4F3`, papel `#FBF5E8`.
- Baloo 2 nos títulos e botões, Nunito no texto, Caveat só no que seria escrito à mão (nome da arte, legenda, assinatura).
- Texto da interface em português do Brasil, só a primeira letra maiúscula, sem emoji e sem ponto de exclamação. Preço no formato `R$ 8,00`.

## Contatos usados nas páginas

WhatsApp `5585982197478`, Instagram `@artesmanuaisartesanais`, Shopee `https://br.shp.ee/ntZ4soXP`. Estão repetidos em cada página; ao trocar um, troque em todas.
