#!/usr/bin/env python3
"""Gera as duas fotos de um produto a partir de uma imagem original.

    python3 .claude/skills/novo-produto/fotos.py <foto-original> <nome-do-arquivo>

Grava img/<nome>.webp (900x1125) e img/<nome>-sm.webp (480x600), em retrato 4:5.
Se a original não for 4:5, corta pelo centro. Não sobrescreve foto que já existe,
a menos que receba --substituir. Precisa do Pillow (pip install Pillow).
"""
import os
import re
import sys

try:
    from PIL import Image, ImageOps
except ImportError:
    sys.exit("Falta o Pillow: pip install Pillow")

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
TAMANHOS = (("", 900, 1125), ("-sm", 480, 600))


def main():
    args = [a for a in sys.argv[1:] if a != "--substituir"]
    substituir = "--substituir" in sys.argv[1:]
    if len(args) != 2:
        sys.exit(__doc__)
    origem, nome = args
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", nome) or nome.endswith("-sm"):
        sys.exit(f"Nome inválido: {nome!r}. Use minúsculas, números e hífen, sem acento (ex.: quadro-girassol).")
    if not os.path.isfile(origem):
        sys.exit(f"Não achei a foto original: {origem}")

    destinos = [os.path.join(RAIZ, "img", f"{nome}{sufixo}.webp") for sufixo, _, _ in TAMANHOS]
    existentes = [d for d in destinos if os.path.exists(d)]
    if existentes and not substituir:
        sys.exit("Já existe: " + ", ".join(os.path.relpath(d, RAIZ) for d in existentes)
                 + ". Escolha outro nome ou passe --substituir.")

    foto = ImageOps.exif_transpose(Image.open(origem)).convert("RGB")
    largura, altura = foto.size
    if largura < 900:
        print(f"Aviso: a original tem {largura} px de largura; a foto de 900 px vai ficar ampliada.", file=sys.stderr)
    proporcao = largura / altura
    if abs(proporcao - 0.8) > 0.01:
        print(f"Aviso: a original é {largura}x{altura}, não 4:5; cortando pelo centro.", file=sys.stderr)

    for (sufixo, w, h), destino in zip(TAMANHOS, destinos):
        ImageOps.fit(foto, (w, h), Image.LANCZOS, centering=(0.5, 0.5)).save(destino, "WEBP", quality=82, method=6)
        print(f"{os.path.relpath(destino, RAIZ)}  {w}x{h}  {os.path.getsize(destino) // 1024} KB")


if __name__ == "__main__":
    main()
