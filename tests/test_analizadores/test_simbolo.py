import pytest
import sys
import os

# Añadir la raíz del proyecto al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from analizadores.simbolo import SimboloAFD

@pytest.fixture
def afd():
    return SimboloAFD()

class TestSimboloAFD:
    def test_operador_aritmetico(self, afd):
        simbolos = ['+', '-', '*', '/', '%']
        for simbolo in simbolos:
            valido, lexema, consumidos = afd.analizar(simbolo, 0)
            assert valido is True
            assert lexema == simbolo
            assert consumidos == len(lexema)
            assert afd.obtener_categoria(lexema) == 'OPERADOR_ARITMETICO'

    def test_operador_comparacion(self, afd):
        simbolos = ['==', '!=', '>', '<', '>=', '<=']
        for simbolo in simbolos:
            valido, lexema, consumidos = afd.analizar(simbolo, 0)
            assert valido is True
            assert lexema == simbolo
            assert consumidos == len(lexema)
            assert afd.obtener_categoria(lexema) == 'OPERADOR_COMPARACION'

    def test_operador_logico(self, afd):
        simbolos = ['&&', '||', '!']
        for simbolo in simbolos:
            valido, lexema, consumidos = afd.analizar(simbolo, 0)
            assert valido is True
            assert lexema == simbolo
            assert consumidos == len(lexema)
            assert afd.obtener_categoria(lexema) == 'OPERADOR_LOGICO'

    def test_operador_asignacion(self, afd):
        simbolos = ['=', '+=', '-=', '*=', '/=', '%=']
        for simbolo in simbolos:
            valido, lexema, consumidos = afd.analizar(simbolo, 0)
            assert valido is True
            assert lexema == simbolo
            assert consumidos == len(lexema)
            assert afd.obtener_categoria(lexema) == 'OPERADOR_ASIGNACION'

    def test_operador_incremento_decremento(self, afd):
        simbolos = ['++', '--']
        for simbolo in simbolos:
            valido, lexema, consumidos = afd.analizar(simbolo, 0)
            assert valido is True
            assert lexema == simbolo
            assert consumidos == len(lexema)
            assert afd.obtener_categoria(lexema) in ['OPERADOR_INCREMENTO', 'OPERADOR_DECREMENTO']

    def test_parentesis(self, afd):
        simbolos = ['(', ')']
        categorias = ['PARENTESIS_APERTURA', 'PARENTESIS_CIERRE']
        for simbolo, categoria in zip(simbolos, categorias):
            valido, lexema, consumidos = afd.analizar(simbolo, 0)
            assert valido is True
            assert lexema == simbolo
            assert consumidos == len(lexema)
            assert afd.obtener_categoria(lexema) == categoria

    def test_llaves(self, afd):
        simbolos = ['{', '}']
        categorias = ['LLAVE_APERTURA', 'LLAVE_CIERRE']
        for simbolo, categoria in zip(simbolos, categorias):
            valido, lexema, consumidos = afd.analizar(simbolo, 0)
            assert valido is True
            assert lexema == simbolo
            assert consumidos == len(lexema)
            assert afd.obtener_categoria(lexema) == categoria

    def test_terminal_separador(self, afd):
        simbolos = [';', ',']
        categorias = ['TERMINAL', 'SEPARADOR']
        for simbolo, categoria in zip(simbolos, categorias):
            valido, lexema, consumidos = afd.analizar(simbolo, 0)
            assert valido is True
            assert lexema == simbolo
            assert consumidos == len(lexema)
            assert afd.obtener_categoria(lexema) == categoria

    def test_no_es_simbolo(self, afd):
        simbolos = ['abc', '123', '@', '#', '$']
        for simbolo in simbolos:
            valido, lexema, consumidos = afd.analizar(simbolo, 0)
            assert valido is False
            assert lexema == ''
            assert consumidos == 0
            assert afd.obtener_categoria(lexema) is None

    def test_cadena_vacia(self, afd):
        valido, lexema, consumidos = afd.analizar('', 0)
        assert valido is False
        assert lexema == ''
        assert consumidos == 0
        assert afd.obtener_categoria(lexema) is None

    def test_simbolo_en_medio(self, afd):
        texto = 'abc+def'
        valido, lexema, consumidos = afd.analizar(texto, 3)
        assert valido is True
        assert lexema == '+'
        assert consumidos == 1
        assert afd.obtener_categoria(lexema) == 'OPERADOR_ARITMETICO'

    def test_simbolo_compuesto_incompleto(self, afd):
        texto = '='
        valido, lexema, consumidos = afd.analizar(texto, 0)
        assert valido is True
        assert lexema == '='
        assert consumidos == 1
        assert afd.obtener_categoria(lexema) == 'OPERADOR_ASIGNACION'

    def test_simbolo_compuesto_completo(self, afd):
        texto = '=='
        valido, lexema, consumidos = afd.analizar(texto, 0)
        assert valido is True
        assert lexema == '=='
        assert consumidos == 2
        assert afd.obtener_categoria(lexema) == 'OPERADOR_COMPARACION' 