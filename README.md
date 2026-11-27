# Artes Manuais Artesanais

Site vitrine da marca **Artes Manuais | Personalizados**: canecas, copos, camisetas e peças sob encomenda feitas à mão em Fortaleza.

O site é uma página estática (`index.html` + pasta `img/`), sem banco de dados, hospedada grátis no GitHub Pages.

## Como adicionar um produto

1. Coloque duas versões da foto em `img/`: `nome.webp` (900 px de largura) e `nome-sm.webp` (480 px), em retrato 4:5.
2. No final do `index.html`, acrescente uma linha na lista `canecas` ou `camisetas`:
   ```js
   ['nome','Frase ou nome da arte','Caneca'],
   ```
3. Salve e envie. O link "Pedir esta no WhatsApp" é gerado sozinho.

## Contatos usados no site

- WhatsApp: (85) 9 8219-7478
- Instagram: @artesmanuaisartesanais
- Shopee: https://br.shp.ee/ntZ4soXP

## Página "Monte seu pedido"

`pedido.html` é o simulador de orçamento: o cliente escolhe as peças, vê o total e envia o pedido pronto no WhatsApp. Preços, estoque dos copos e a lista de peças ficam no começo do `<script>` (constantes `PRODUTOS` e `ENCOMENDA`). Ao cadastrar um produto novo no site, acrescente-o também ali.

## Página "Loja" (vitrine + sacola + Pix)

`loja.html` é a vitrine com sacola: a cliente filtra por categoria, escolhe cor/tamanho, monta a sacola, paga com **Pix copia e cola / QR Code** e envia o pedido organizado no WhatsApp (com código `AM-XXXX`).

- Configuração no começo do `<script>`: `PIX` (chave CNPJ, nome, cidade), `PIX_DESCONTO` (0 = sem desconto), `PRODUTOS` e `CATS`.
- O Pix é **estático**: o código já vem com o valor das peças, mas **não há confirmação automática**. Confira o recebimento no extrato antes de produzir.
- Frete e itens "a combinar" ficam fora do valor do Pix e são acertados no WhatsApp.
- O QR Code usa `js/qrcode.js` (biblioteca qrcode-generator, licença MIT), incluída no repositório.
- A lista de produtos hoje está repetida em `index.html`, `pedido.html` e `loja.html`: ao cadastrar um produto, atualize as três.
