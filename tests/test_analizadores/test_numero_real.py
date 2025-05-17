import pytest
import sys
import os

# Añadir la raíz del proyecto al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from analizadores.numero_real import NumeroRealAFD

@pytest.fixture
def afd():
    return NumeroRealAFD()

class TestNumeroRealAFD:
    def test_reales_validos(self, afd):
        casos = [
            ("123.45", True, "123.45", 6),
            ("0.5", True, "0.5", 3),
            (".5", True, ".5", 2),
            ("123e10", True, "123e10", 6),
            ("123.45e-10", True, "123.45e-10", 10),
            ("123.", True, "123.", 4),
            ("1e10", True, "1e10", 4),
            (".5e2", True, ".5e2", 4),
            ("0.0", True, "0.0", 3),
        ]
        for texto, esperado_valido, esperado_lexema, esperado_consumidos in casos:
            valido, lexema, consumidos = afd.analizar(texto, 0)
            assert valido is esperado_valido
            assert lexema == esperado_lexema
            assert consumidos == esperado_consumidos

    def test_reales_con_texto(self, afd):
        casos = [
            ("123.45abc", True, "123.45", 6),
            (".5xyz", True, ".5", 2),
            ("1e10resto", True, "1e10", 4),
            ("0.5extra", True, "0.5", 3),
        ]
        for texto, esperado_valido, esperado_lexema, esperado_consumidos in casos:
            valido, lexema, consumidos = afd.analizar(texto, 0)
            assert valido is esperado_valido
            assert lexema == esperado_lexema
            assert consumidos == esperado_consumidos

    def test_reales_invalidos(self, afd):
        casos = [
            ("123", False, "", 0),
            ("abc", False, "", 0),
            ("", False, "", 0),
            ("123e", False, "", 0),
            ("123e+", False, "", 0),
            ("e10", False, "", 0),
            ("123.45.67", True, "123.45", 6),  # Solo reconoce hasta el segundo punto
            (".e2", False, "", 0),
            (".e", False, "", 0),
        ]
        for texto, esperado_valido, esperado_lexema, esperado_consumidos in casos:
            valido, lexema, consumidos = afd.analizar(texto, 0)
            assert valido is esperado_valido
            assert lexema == esperado_lexema
            assert consumidos == esperado_consumidos 