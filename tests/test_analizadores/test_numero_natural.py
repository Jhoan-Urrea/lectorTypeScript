import pytest
import sys
import os

# Añadir la raíz del proyecto al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from analizadores.numero_natural import NumeroNaturalAFD

@pytest.fixture
def afd():
    return NumeroNaturalAFD()

class TestNumeroNaturalAFD:
    def test_numero_natural_valido(self, afd):
        casos = [
            ("123", True, "123", 3),
            ("456789", True, "456789", 6),
            ("0", True, "0", 1),
            ("9876543210", True, "9876543210", 10),
        ]
        for texto, esperado_valido, esperado_lexema, esperado_consumidos in casos:
            valido, lexema, consumidos = afd.analizar(texto, 0)
            assert valido is esperado_valido
            assert lexema == esperado_lexema
            assert consumidos == esperado_consumidos

    def test_numero_natural_con_texto(self, afd):
        casos = [
            ("123abc", True, "123", 3),
            ("0abc", True, "0", 1),
            ("4567xyz", True, "4567", 4),
        ]
        for texto, esperado_valido, esperado_lexema, esperado_consumidos in casos:
            valido, lexema, consumidos = afd.analizar(texto, 0)
            assert valido is esperado_valido
            assert lexema == esperado_lexema
            assert consumidos == esperado_consumidos

    def test_numero_natural_no_valido(self, afd):
        casos = [
            ("abc", False, "", 0),
            ("", False, "", 0),
            ("a123", False, "", 0),
            ("-123", False, "", 0),
        ]
        for texto, esperado_valido, esperado_lexema, esperado_consumidos in casos:
            valido, lexema, consumidos = afd.analizar(texto, 0)
            assert valido is esperado_valido
            assert lexema == esperado_lexema
            assert consumidos == esperado_consumidos

    def test_numero_natural_ceros_a_la_izquierda(self, afd):
        casos = [
            ("01", True, "0", 1),
            ("00123", True, "0", 1),
            ("000", True, "0", 1),
        ]
        for texto, esperado_valido, esperado_lexema, esperado_consumidos in casos:
            valido, lexema, consumidos = afd.analizar(texto, 0)
            assert valido is esperado_valido
            assert lexema == esperado_lexema
            assert consumidos == esperado_consumidos 