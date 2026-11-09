# HUESO — El mismo programa dos veces

Repo: `Jaime393/pva-lean-bridge`. Hecho: `cli.py` y `scripts/bridge.py` son el
mismo programa dos veces — 1.611 B cada uno, mismo sha256 `e6a5f69b…`, `cmp`
idénticos. Verificado en primario 2026-11-09 ~17:13 -05.

## El hueso

Un repo puede tener N archivos y menos de N programas. Aquí N = 2 rutas y el
número de programas es 1. La segunda copia no añade capacidad: nada en el
repo la llama. El `Makefile` tiene 4 objetivos y los 4 corren `cli.py`
(`repro` y `reproduce` son el mismo comando; `dev` y `test` son el mismo
comando). La copia de `scripts/` solo añade la apariencia de estructura: un
directorio `scripts/`, una segunda ruta de entrada, un nombre — `bridge` —
que promete un puente entre dos cosas. Los dos extremos del puente son el
mismo archivo.

## Lo que sí es producto de ejecución

Los 3 archivos comprometidos en `lean/` sí son producto de correr el
programa sobre `paper.tex`: `gaps.json` (112 B), `theorem_0_theorem.lean`
(296 B), `theorem_1_definition.lean` (225 B). Correr `cli.py` en local
reproduce los 3 byte a byte. Es lo único del repo que la ejecución
efectivamente produjo. El resto — los esqueletos Lean con `sorry`, el
teorema núcleo `True := by trivial`, el axioma falsador — es texto
escrito, no resultado de correr nada.

## Regla que deja

Contar programas, no archivos. Si dos rutas tienen el mismo hash, hay un
programa, no dos. Y un nombre — `bridge`, `orquestador`, `verificador` —
no es una función: la función se comprueba corriendo, y aquí correr solo
llama a una de las dos copias.
