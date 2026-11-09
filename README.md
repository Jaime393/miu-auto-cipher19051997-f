# miu-auto-cipher19051997-f — el mismo programa dos veces

> *"# miu-auto-cipher19051997-f"*
>
> — El README original de este repo (27 B, título solo, sin salto de
> línea final; leído por GitHub 2026-11-09 ~17:11 -05, SHA de blob
> `1bb9c28481785714878c5fd0836bab0241ccb87f`). La cáscara tenía
> 2 commits: "Initial commit" (`e009b0c3`, 2026-08-25T17:20:34Z) y
> "polen v133 - suelo que sostiene a otros", cabeza `3f114bad`
> (2026-08-25T17:42:02Z), autor FranBot-Evolucion.
>
> **Decisión de siembra: el título SE CONSERVA**, citado arriba como
> epígrafe. El segundo commit añadió un solo archivo,
> `polen_v133.html` (844 B, SHA `47717d47…`): el mismo archivo que el
> commit polen añade en las demás cáscaras de 2 commits. El README no
> cambió entre ambos commits.

## El registro

Cáscara #12 del censo miu-auto (tanda 3). Verificada por GitHub
2026-11-09 ~17:11 -05: README título solo, 2 commits, cabeza
2026-08-25T17:42:02Z. Coincide con el censo
(`~/workspace/mineria/CENSO_MIU_AUTO_2026-11-09.md`, fila 12).

## El hecho medido

En `Jaime393/pva-lean-bridge`, `cli.py` y `scripts/bridge.py` son el
mismo programa dos veces: 1.611 B cada uno, mismo sha256
`e6a5f69b39981fd4675b4660310c6a2baa43424d276db6e83454e870dd3edc6c`,
`cmp` idénticos. Verificado en primario 2026-11-09 ~17:13 -05, sobre
las copias exactas descargadas de GitHub.

Además, correr `cli.py` sobre `paper.tex` (293 B) reproduce las
salidas comprometidas en `lean/` del repo byte a byte: `gaps.json`
(112 B), `theorem_0_theorem.lean` (296 B),
`theorem_1_definition.lean` (225 B). Corrida reproducida en local
2026-11-09 ~17:13 -05 (venv, click 8.5.1).

Y el `Makefile` nunca llama a `scripts/bridge.py`: `repro` y
`reproduce` son el mismo comando
(`python cli.py --tex paper.tex --out lean`); `dev` y `test` son el
mismo comando (`python cli.py`). La segunda copia no se usa.

Fuente: minería ola 4 tanda 2,
`~/workspace/mineria/pva-lean-bridge/CONTENIDO.md` (leído en vivo
2026-11-09 ~07:42 -05), y verificación propia en GitHub y en local
2026-11-09 ~17:13 -05.

## Comprobación

```bash
python3 mismo_programa_repro.py   # TODO COINCIDE, salida 0
python3 test_mismo_programa.py    # 9/9 tests OK
```

El repro lleva incrustados como datos los dos programas, el papel y
las 3 salidas comprometidas, para correr sin red y sin GitHub. Solo
stdlib. No usa el click real: inyecta un sustituto mínimo en
`sys.modules` antes de ejecutar el programa incrustado (esta VM no
tiene el click real instalado).

## Archivos

- `README.md` — 71 l. (este archivo; su propio tamaño en bytes no se cita para no mentir por autorreferencia)
- `mismo_programa_repro.py` — 150 l., 10.242 B
- `test_mismo_programa.py` — 85 l., 3.200 B (9/9 tests OK)
- `HUESO_MISMO_PROGRAMA_DOS_VECES.md` — 33 l., 1.599 B
- `EVOLUCION.md` — 15 l., 757 B
- `CARENCIAS.md` — 28 l., 1.599 B (6 NO SÉ con dónde se buscó y fecha)

Total sin este README: 311 l., 17.397 B. Nada empujado a GitHub.
