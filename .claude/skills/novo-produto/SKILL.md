---
name: novo-produto
description: Cadastra um produto novo no site (fotos em img/ e a linha em index.html, pedido.html e loja.html). Use quando pedirem para adicionar uma caneca, copo, camiseta, quadro, botton, ímã ou enfeite.
disable-model-invocation: true
argument-hint: "<foto> <categoria> <nome da arte> <preço>"
---

# Novo produto

Cadastra um produto nas três páginas do site e gera as duas fotos. O que entra em `main` vai ao ar, então o trabalho termina num branch com PR, nunca direto em `main`.

Pedido recebido: $ARGUMENTS

## 1. Junte os dados

Você precisa de cinco coisas. O que faltar no pedido, pergunte de uma vez só, antes de mexer em qualquer arquivo. Não invente preço, nome nem estoque.

| Dado | Observação |
| --- | --- |
| Foto original | Caminho do arquivo. Em retrato; se não for 4:5, o corte é pelo centro. |
| Categoria | `canecas`, `copos`, `camisetas`, `quadros`, `bottons`, `imas` ou `natal`. |
| Nome da arte | A frase da peça, escrita como no pedido. Pode ficar vazio; nesse caso peça uma descrição curta (ex.: "caderno rosa"). |
| Preço | Em reais. O mesmo nas três páginas. |
| Peça única ou sob demanda | Peça pronta leva `estoque` e `pronta:true`. Camiseta e caneca feitas por pedido não levam. |

O nome do arquivo você decide: minúsculas, sem acento, palavras ligadas por hífen, curto (`quadro-girassol`, `botton-luffy`, `ima-totoro`). Siga o prefixo que a categoria já usa (`botton-`, `ima-`, `natal-NN`). Confira que ainda não existe em `img/`.

Se o pedido for uma cor nova de um produto que já existe, vá para a seção "Variação de cor".

## 2. Gere as fotos

```bash
python3 .claude/skills/novo-produto/fotos.py <foto-original> <nome-do-arquivo>
```

Grava `img/<nome>.webp` (900×1125) e `img/<nome>-sm.webp` (480×600). O script avisa se cortou a foto ou se a original é pequena; nesse caso, abra a foto gerada e confira que a arte não foi cortada antes de seguir. Se cortou, peça outra foto em vez de publicar.

## 3. Acrescente nas três páginas

Leia as linhas vizinhas da mesma categoria em cada arquivo antes de escrever e copie o formato delas, inclusive o tipo de aspas. Acrescente no fim do bloco da categoria.

**`index.html`**, na lista da categoria (`canecas`, `camisetas`, `quadros`, `bottons`, `imas`, `natal`; copos ficam em `canecas`):

```js
['nome-do-arquivo',"Nome da arte",'Tipo',25],
['nome-do-arquivo','','Tipo',25,'descrição curta'],   // quando não há nome
```

O preço é opcional aqui: só entra se os vizinhos da categoria mostram preço.

**`pedido.html`**, em `PRODUTOS`, no bloco da categoria:

```js
C("nome-do-arquivo","Tipo","Nome da arte",25,{estoque:1,pronta:true}),
```

**`loja.html`**, em `PRODUTOS`:

```js
P("nome-do-arquivo","categoria","Tipo","Nome da arte",25,{estoque:1,pronta:true}),
```

A categoria em `loja.html` precisa ser um `id` que exista em `CATS`. O "Tipo" é o texto que aparece para a cliente ("Caneca", "Copo americano", "Quadro", "Enfeite de Natal"); use o mesmo dos vizinhos.

### Variação de cor

Cor nova de um produto existente não vira produto novo em `pedido.html` nem em `loja.html`: entra em `fotoCor` (e em `cores`, quando houver) do produto principal. Em `index.html` ganha linha própria. Veja `estrela-marrom` e `nordeste-preta` como modelo.

## 4. Confira

```bash
python3 .claude/hooks/confere-produtos.py
```

Tem de sair sem nada. Se acusar algo, corrija e rode de novo.

Depois suba o site (`python3 -m http.server 8765`) e abra as três páginas no navegador: o produto aparece na categoria certa, a foto carrega, o nome e o preço estão iguais nas três, e o link "Pedir esta no WhatsApp" de `index.html` leva o tipo, o nome e o preço na mensagem. Tire um print de cada página com o produto visível.

## 5. Entregue

Commit no branch de trabalho com a mensagem no padrão do repositório, por exemplo `Adiciona quadro Cigana (R$ 25,00)`, push e PR em rascunho. No resumo, diga o nome do arquivo escolhido, o que entrou em cada página, e mostre os prints. Se algum dado foi presumido, diga qual.
