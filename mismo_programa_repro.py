#!/usr/bin/env python3
"""Reproduce el hecho: cli.py y scripts/bridge.py de pva-lean-bridge son el mismo programa dos veces.

Hecho verificado en primario 2026-11-09 ~17:13 -05 (GitHub, owner Jaime393, repo pva-lean-bridge):
- cli.py y scripts/bridge.py miden 1.611 B cada uno, sha256 e6a5f69b39981fd4675b4660310c6a2baa43424d276db6e83454e870dd3edc6c, cmp identicos.
- Correr cli.py sobre paper.tex genera 2 esqueletos; los 3 archivos de salida son byte a byte
  identicos a los comprometidos en lean/ del repo (gaps.json 112 B, theorem_0_theorem.lean 296 B,
  theorem_1_definition.lean 225 B). Corrida reproducida en local 2026-11-09 ~17:13 -05
  (venv, click 8.5.1, sobre las copias exactas descargadas de GitHub).
- El Makefile nunca llama a scripts/bridge.py: repro y reproduce son el mismo comando
  (python cli.py --tex paper.tex --out lean); dev y test son el mismo comando (python cli.py).

Los textos de los programas y de los archivos comprometidos van incrustados como datos,
para que este repro corra sin red y sin GitHub. Solo stdlib. No usa el click real:
inyecta un sustituto minimo en sys.modules antes de ejecutar el programa incrustado.
"""

import hashlib
import json
import sys
import tempfile
from pathlib import Path

CLI_SHA256 = "e6a5f69b39981fd4675b4660310c6a2baa43424d276db6e83454e870dd3edc6c"
CLI_BYTES = 1611
PAPER_SHA256 = "bc50c89a395de50a8953a146c12fb1dcd950c92b83950df63cd923e1f1adc89a"
PAPER_BYTES = 293
ESPERADO = {
    "gaps.json": (112, "904b5dd2253b70b71acaf8130f8a0cbe95d8d66a976f35f6e8c4adb244ca3cef"),
    "theorem_0_theorem.lean": (296, "ad76c34f5570ffc11bb3b1ba58ed1cc8e5c3064d0cc913a395324e053aac1642"),
    "theorem_1_definition.lean": (225, "cba60484f5a946364471e70b70f974c3cc31786d3f22557b5ce5dade4fbeb4e9"),
}

CLI_TEXT = '#!/usr/bin/env python3\n# pva-lean-bridge V202 — LaTeX -> Lean4 esqueleto — rho(x)>0\nimport re, pathlib, click, json\nfrom pathlib import Path\n\ndef extract_theorems(tex_path):\n    text = Path(tex_path).read_text(errors=\'ignore\')\n    # busca \\begin{theorem} ... \\end{theorem} o \\begin{definition}\n    pattern = r\'\\\\begin\\{(theorem|lemma|definition|proposition)\\}(.*?)\\\\end\\{\\1\\}\'\n    matches = re.findall(pattern, text, re.DOTALL)\n    return matches\n\ndef gen_lean_skeleton(name, body):\n    return f\'\'\'import Mathlib\n\n-- {name} extraido de LaTeX\n-- TODO: formalizar\n\ntheorem {name}_placeholder : True := by\n  trivial\n\n-- cuerpo original LaTeX:\n-- {body[:200]}...\n\'\'\'\n\n@click.command()\n@click.option("--tex", default="paper.tex", help="Paper LaTeX")\n@click.option("--out", default="lean", help="Out dir")\ndef main(tex, out):\n    p = Path(tex)\n    if not p.exists():\n        print(f"No existe {tex}, creando ejemplo Navier-Stokes")\n        Path(tex).write_text(r"\\begin{theorem}[Navier-Stokes Clay]\\n Existe solucion suave... \\end{theorem}")\n    thms = extract_theorems(tex)\n    Path(out).mkdir(exist_ok=True)\n    for i,(kind,body) in enumerate(thms):\n        name = f"theorem_{i}_{kind}"\n        (Path(out)/f"{name}.lean").write_text(gen_lean_skeleton(name, body))\n    print(f"Generados {len(thms)} esqueletos en {out}/")\n    # genera informe brechas\n    report = {"theorems": len(thms), "gaps": ["definir Sobolev", "definir solucion debil", "definir suavidad"]}\n    Path(f"{out}/gaps.json").write_text(json.dumps(report, indent=2))\n    print(json.dumps(report, indent=2))\n\nif __name__ == "__main__":\n    main()\n'
BRIDGE_TEXT = '#!/usr/bin/env python3\n# pva-lean-bridge V202 — LaTeX -> Lean4 esqueleto — rho(x)>0\nimport re, pathlib, click, json\nfrom pathlib import Path\n\ndef extract_theorems(tex_path):\n    text = Path(tex_path).read_text(errors=\'ignore\')\n    # busca \\begin{theorem} ... \\end{theorem} o \\begin{definition}\n    pattern = r\'\\\\begin\\{(theorem|lemma|definition|proposition)\\}(.*?)\\\\end\\{\\1\\}\'\n    matches = re.findall(pattern, text, re.DOTALL)\n    return matches\n\ndef gen_lean_skeleton(name, body):\n    return f\'\'\'import Mathlib\n\n-- {name} extraido de LaTeX\n-- TODO: formalizar\n\ntheorem {name}_placeholder : True := by\n  trivial\n\n-- cuerpo original LaTeX:\n-- {body[:200]}...\n\'\'\'\n\n@click.command()\n@click.option("--tex", default="paper.tex", help="Paper LaTeX")\n@click.option("--out", default="lean", help="Out dir")\ndef main(tex, out):\n    p = Path(tex)\n    if not p.exists():\n        print(f"No existe {tex}, creando ejemplo Navier-Stokes")\n        Path(tex).write_text(r"\\begin{theorem}[Navier-Stokes Clay]\\n Existe solucion suave... \\end{theorem}")\n    thms = extract_theorems(tex)\n    Path(out).mkdir(exist_ok=True)\n    for i,(kind,body) in enumerate(thms):\n        name = f"theorem_{i}_{kind}"\n        (Path(out)/f"{name}.lean").write_text(gen_lean_skeleton(name, body))\n    print(f"Generados {len(thms)} esqueletos en {out}/")\n    # genera informe brechas\n    report = {"theorems": len(thms), "gaps": ["definir Sobolev", "definir solucion debil", "definir suavidad"]}\n    Path(f"{out}/gaps.json").write_text(json.dumps(report, indent=2))\n    print(json.dumps(report, indent=2))\n\nif __name__ == "__main__":\n    main()\n'
PAPER_TEX = '\\documentclass{article}\n\\begin{document}\n\\begin{theorem}[Navier-Stokes Clay]\nSea $u_0$ campo inicial suave divergencia cero. Entonces existe solucion suave global de Navier-Stokes.\n\\end{theorem}\n\\begin{definition}[Sobolev H1]\n$H^1$ funciones con derivada L2...\n\\end{definition}\n\\end{document}\n'
ESPERADO_GAPS_JSON = '{\n  "theorems": 2,\n  "gaps": [\n    "definir Sobolev",\n    "definir solucion debil",\n    "definir suavidad"\n  ]\n}'
ESPERADO_T0 = 'import Mathlib\n\n-- theorem_0_theorem extraido de LaTeX\n-- TODO: formalizar\n\ntheorem theorem_0_theorem_placeholder : True := by\n  trivial\n\n-- cuerpo original LaTeX:\n-- [Navier-Stokes Clay]\nSea $u_0$ campo inicial suave divergencia cero. Entonces existe solucion suave global de Navier-Stokes.\n...\n'
ESPERADO_T1 = 'import Mathlib\n\n-- theorem_1_definition extraido de LaTeX\n-- TODO: formalizar\n\ntheorem theorem_1_definition_placeholder : True := by\n  trivial\n\n-- cuerpo original LaTeX:\n-- [Sobolev H1]\n$H^1$ funciones con derivada L2...\n...\n'


def _sha(text):
    return hashlib.sha256(text.encode()).hexdigest()


class _ClickComando:
    """Sustituto minimo de click.command: parsea --tex y --out de sys.argv."""

    def __init__(self, fn):
        self.fn = fn

    def __call__(self):
        tex, out = "paper.tex", "lean"
        args = sys.argv[1:]
        i = 0
        while i < len(args):
            if args[i] == "--tex" and i + 1 < len(args):
                tex = args[i + 1]
                i += 2
            elif args[i] == "--out" and i + 1 < len(args):
                out = args[i + 1]
                i += 2
            elif args[i].startswith("--tex="):
                tex = args[i][6:]
                i += 1
            elif args[i].startswith("--out="):
                out = args[i][6:]
                i += 1
            else:
                i += 1
        return self.fn(tex=tex, out=out)


class _ClickFalso:
    """Sustituto minimo del modulo click: option no hace nada, command envuelve."""

    @staticmethod
    def option(*args, **kwargs):
        def deco(fn):
            return fn

        return deco

    @staticmethod
    def command(*args, **kwargs):
        def deco(fn):
            return _ClickComando(fn)

        return deco


def main():
    ok = True

    def check(nombre, cond, detalle=""):
        nonlocal ok
        print(("OK   " if cond else "FALLO") + " " + nombre + (" — " + detalle if detalle else ""))
        if not cond:
            ok = False

    check("cli.py mide 1611 B", len(CLI_TEXT.encode()) == CLI_BYTES,
          f"mide {len(CLI_TEXT.encode())} B")
    check("scripts/bridge.py mide 1611 B", len(BRIDGE_TEXT.encode()) == CLI_BYTES,
          f"mide {len(BRIDGE_TEXT.encode())} B")
    check("cli.py sha256 e6a5f69b…", _sha(CLI_TEXT) == CLI_SHA256, _sha(CLI_TEXT)[:12])
    check("scripts/bridge.py sha256 e6a5f69b…", _sha(BRIDGE_TEXT) == CLI_SHA256,
          _sha(BRIDGE_TEXT)[:12])
    check("cli.py == scripts/bridge.py (texto identico)", CLI_TEXT == BRIDGE_TEXT)
    check("paper.tex mide 293 B", len(PAPER_TEX.encode()) == PAPER_BYTES,
          f"mide {len(PAPER_TEX.encode())} B")
    check("paper.tex sha256 bc50c89a…", _sha(PAPER_TEX) == PAPER_SHA256, _sha(PAPER_TEX)[:12])

    # Corrida del programa incrustado sobre el papel incrustado, con el
    # sustituto de click (esta VM no tiene el click real instalado).
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        (tmp / "paper.tex").write_text(PAPER_TEX)
        out_dir = tmp / "out"
        viejo_argv = sys.argv
        viejo_click = sys.modules.get("click")
        sys.modules["click"] = _ClickFalso
        sys.argv = ["cli.py", "--tex", str(tmp / "paper.tex"), "--out", str(out_dir)]
        try:
            exec(compile(CLI_TEXT, "cli.py", "exec"), {"__name__": "__main__"})
        finally:
            sys.argv = viejo_argv
            if viejo_click is None:
                sys.modules.pop("click", None)
            else:
                sys.modules["click"] = viejo_click
        generados = sorted(p.name for p in out_dir.iterdir())
        check("la corrida genera 3 archivos", generados == ["gaps.json", "theorem_0_theorem.lean",
                                                             "theorem_1_definition.lean"],
              ", ".join(generados))
        esperado_texto = {"gaps.json": ESPERADO_GAPS_JSON,
                          "theorem_0_theorem.lean": ESPERADO_T0,
                          "theorem_1_definition.lean": ESPERADO_T1}
        for nombre, (tam, suma) in ESPERADO.items():
            texto = (out_dir / nombre).read_text()
            check(f"{nombre} mide {tam} B", len(texto.encode()) == tam,
                  f"mide {len(texto.encode())} B")
            check(f"{nombre} sha256 {suma[:8]}…", _sha(texto) == suma, _sha(texto)[:12])
            check(f"{nombre} identico al comprometido", texto == esperado_texto[nombre])

    print("TODO COINCIDE" if ok else "NO COINCIDE")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
