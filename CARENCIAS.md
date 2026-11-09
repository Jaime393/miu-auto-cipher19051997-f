# CARENCIAS

Lo que esta semilla no sabe. Cada NO SÉ dice dónde se buscó y cuándo.

1. **Por qué el repo lleva el mismo programa dos veces.** NO SÉ. Ningún
   archivo lo explica: buscado en `README.md`, `Makefile` y los 5
   archivos de minería de `pva-lean-bridge`
   (`~/workspace/mineria/pva-lean-bridge/`, leídos 2026-11-09 ~17:12 -05).
2. **Si `scripts/bridge.py` se ejecuta alguna vez.** NO SÉ. Nada en el
   repo lo llama: los 4 objetivos del `Makefile` corren `cli.py`
   (`repro`/`reproduce`: `python cli.py --tex paper.tex --out lean`;
   `dev`/`test`: `python cli.py`). Leído en GitHub 2026-11-09 ~17:13 -05.
   Que nada lo llame no prueba que nadie lo haya corrido nunca fuera
   del repo.
3. **Si el workflow `pva.yml` corrió alguna vez.** NO SÉ. La minería no
   lo verificó corriendo (`CONTENIDO.md`, 2026-11-09 ~07:42 -05); no se
   re-verificó aquí.
4. **Si `lake build` corrió alguna vez.** NO SÉ. Lean no está instalado
   en esta máquina (`which lean lake elan`: nada; minería 2026-11-09
   ~07:42 -05). El `lakefile.lean` no declara dependencias (`require`),
   mientras los `.lean` hacen `import Mathlib`.
5. **Si existe algún papel distinto de `paper.tex` que el puente haya
   convertido.** NO SÉ. `paper.tex` (293 B) es el único archivo de
   entrada del repo (listado del árbol en GitHub, 2026-11-09 ~17:12 -05)
   y los 3 archivos comprometidos en `lean/` salen de él.
6. **De dónde sale "Phi 9158.79" en la cabecera de
   `lean/KiPhiBeta.lean`.** NO SÉ. Sin derivación en ningún archivo
   (minería `CONTENIDO.md`, 2026-11-09 ~07:42 -05).
