#!/usr/bin/env python3
"""Tests de la semilla miu-auto-cipher19051997-f: cli.py y scripts/bridge.py
de pva-lean-bridge son el mismo programa dos veces.

Corre con: python3 test_mismo_programa.py (stdlib, sin red, sin click real).
"""

import io
import subprocess
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path

import mismo_programa_repro as repro

DIR = Path(__file__).parent


class TestMismoPrograma(unittest.TestCase):
    def test_tamanios(self):
        self.assertEqual(len(repro.CLI_TEXT.encode()), 1611)
        self.assertEqual(len(repro.BRIDGE_TEXT.encode()), 1611)

    def test_sha256_cli(self):
        self.assertEqual(repro._sha(repro.CLI_TEXT),
                         "e6a5f69b39981fd4675b4660310c6a2baa43424d276db6e83454e870dd3edc6c")

    def test_sha256_bridge(self):
        self.assertEqual(repro._sha(repro.BRIDGE_TEXT),
                         "e6a5f69b39981fd4675b4660310c6a2baa43424d276db6e83454e870dd3edc6c")

    def test_identicos(self):
        self.assertEqual(repro.CLI_TEXT, repro.BRIDGE_TEXT)

    def test_paper_tex(self):
        self.assertEqual(len(repro.PAPER_TEX.encode()), 293)
        self.assertEqual(repro._sha(repro.PAPER_TEX),
                         "bc50c89a395de50a8953a146c12fb1dcd950c92b83950df63cd923e1f1adc89a")

    def test_salidas_esperadas(self):
        self.assertEqual(len(repro.ESPERADO_GAPS_JSON.encode()), 112)
        self.assertEqual(repro._sha(repro.ESPERADO_GAPS_JSON),
                         "904b5dd2253b70b71acaf8130f8a0cbe95d8d66a976f35f6e8c4adb244ca3cef")
        self.assertEqual(len(repro.ESPERADO_T0.encode()), 296)
        self.assertEqual(repro._sha(repro.ESPERADO_T0),
                         "ad76c34f5570ffc11bb3b1ba58ed1cc8e5c3064d0cc913a395324e053aac1642")
        self.assertEqual(len(repro.ESPERADO_T1.encode()), 225)
        self.assertEqual(repro._sha(repro.ESPERADO_T1),
                         "cba60484f5a946364471e70b70f974c3cc31786d3f22557b5ce5dade4fbeb4e9")

    def test_repro_main(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = repro.main()
        self.assertEqual(rc, 0)
        self.assertIn("TODO COINCIDE", buf.getvalue())

    def test_repro_como_proceso(self):
        proc = subprocess.run([sys.executable, str(DIR / "mismo_programa_repro.py")],
                              capture_output=True, text=True, timeout=60)
        self.assertEqual(proc.returncode, 0)
        self.assertIn("TODO COINCIDE", proc.stdout)

    def test_funciona_sin_click_real(self):
        # El repro no depende del click real: lo sustituye en sys.modules.
        # Se comprueba bloqueando la importación de click y re-corriendo.
        import importlib
        viejo = sys.modules.get("click")
        sys.modules["click"] = None
        try:
            importlib.reload(repro)
            buf = io.StringIO()
            with redirect_stdout(buf):
                rc = repro.main()
        finally:
            if viejo is None:
                sys.modules.pop("click", None)
            else:
                sys.modules["click"] = viejo
        self.assertEqual(rc, 0)


if __name__ == "__main__":
    unittest.main()
