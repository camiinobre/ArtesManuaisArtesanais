#!/usr/bin/env python3
"""Confere se as listas de produtos das páginas batem entre si e com as fotos.

Roda sozinho depois que o Claude edita index.html, pedido.html, loja.html ou algo
em img/ (ver .claude/settings.json). Também dá para rodar à mão:

    python3 .claude/hooks/confere-produtos.py

Sai com 0 se está tudo certo e com 2 (lista no stderr) se achou divergência.
"""
import json
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PAGINAS = {"index.html", "pedido.html", "loja.html"}


def veio_de_edicao_irrelevante():
    """True quando o hook foi chamado por uma edição que não mexe em produto."""
    if sys.stdin.isatty():
        return False
    try:
        dados = json.load(sys.stdin)
    except ValueError:
        return False
    caminho = (dados.get("tool_input") or {}).get("file_path") or ""
    if not caminho:
        return False
    rel = os.path.relpath(os.path.abspath(caminho), RAIZ)
    return rel not in PAGINAS and not rel.startswith("img" + os.sep)


def ler(nome):
    caminho = os.path.join(RAIZ, nome)
    if not os.path.exists(caminho):
        return ""
    with open(caminho, encoding="utf-8") as f:
        return f.read()


def fotos_de_cor(texto):
    ids = set()
    for bloco in re.findall(r"fotoCor:\{([^}]*)\}", texto):
        ids.update(re.findall(r'"([a-z0-9-]+)"', bloco))
    return ids


def main():
    if veio_de_edicao_irrelevante():
        return 0

    index, pedido, loja = ler("index.html"), ler("pedido.html"), ler("loja.html")
    problemas = []

    # index.html: ['arquivo','Nome','Tipo',preco,'descricao']
    vitrine = {}
    texto = r"""(?:'(?:[^'\\]|\\.)*'|"(?:[^"\\]|\\.)*")"""  # campo entre aspas simples ou duplas
    for m in re.finditer(r"^\s*\['([a-z0-9-]+)'," + texto + "," + texto + r"(?:,([0-9.]+))?", index, re.M):
        vitrine[m.group(1)] = float(m.group(2)) if m.group(2) else None

    # pedido.html: C("arquivo","Tipo","Nome",preco,{...})
    simulador = {m.group(1): float(m.group(2))
                 for m in re.finditer(r'C\("([a-z0-9-]+)","[^"]*","[^"]*",([0-9.]+)', pedido)}
    fotos_simulador = set(simulador) | fotos_de_cor(pedido)

    # loja.html: P("arquivo","categoria","Tipo","Nome",preco,{...})
    sacola, fotos_loja = {}, set(fotos_de_cor(loja))
    for linha in loja.splitlines():
        m = re.match(r'\s*P\("([a-z0-9-]+)","([a-z0-9-]+)","[^"]*","[^"]*",([0-9.]+)', linha)
        if not m:
            continue
        pid, cat, preco = m.group(1), m.group(2), float(m.group(3))
        foto = re.search(r'foto:(null|"([a-z0-9-]+)")', linha)
        if foto is None:
            fotos_loja.add(pid)
        elif foto.group(2):
            fotos_loja.add(foto.group(2))
        if cat != "encomenda":
            sacola[pid] = preco

    if vitrine and simulador:
        for pid in sorted(set(vitrine) - fotos_simulador):
            problemas.append(f"{pid}: está em index.html e falta em PRODUTOS de pedido.html")
        for pid in sorted(fotos_simulador - set(vitrine)):
            problemas.append(f"{pid}: está em pedido.html e falta na lista de index.html")
        for pid in sorted(set(vitrine) & set(simulador)):
            if vitrine[pid] is not None and vitrine[pid] != simulador[pid]:
                problemas.append(f"{pid}: preço {vitrine[pid]:g} em index.html e {simulador[pid]:g} em pedido.html")

    if vitrine and sacola:
        for pid in sorted(set(vitrine) - fotos_loja):
            problemas.append(f"{pid}: está em index.html e falta em PRODUTOS de loja.html")
    for pid in sorted(sacola):
        if vitrine and pid not in vitrine:
            problemas.append(f"{pid}: está em loja.html e falta na lista de index.html")
        if pid in simulador and sacola[pid] != simulador[pid]:
            problemas.append(f"{pid}: preço {sacola[pid]:g} em loja.html e {simulador[pid]:g} em pedido.html")

    for pid in sorted(set(vitrine) | fotos_simulador | fotos_loja):
        for arquivo in (f"{pid}.webp", f"{pid}-sm.webp"):
            if not os.path.exists(os.path.join(RAIZ, "img", arquivo)):
                problemas.append(f"img/{arquivo}: foto não existe")

    if problemas:
        print("Listas de produtos fora de sincronia:", file=sys.stderr)
        for p in problemas:
            print(f"  - {p}", file=sys.stderr)
        print("Corrija antes de terminar (ver CLAUDE.md, seção Produto novo).", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
