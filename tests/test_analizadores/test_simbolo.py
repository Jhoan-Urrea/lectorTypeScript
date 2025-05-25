import pytest
import sys
import os

# Añadir la raíz del proyecto al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from analizadores.simbolo import SimboloAFD
from tokens import Categoria

@pytest.fixture
def afd():
    return SimboloAFD()

class TestSimboloAFD:
    def test_operador_aritmetico(self, afd):
        simbolos = ['+', '-', '*', '/', '%', '**']
        for simbolo in simbolos:
            valido, lexema, consumidos, categoria = afd.analizar(simbolo, 0)
            assert valido is True
            assert lexema == simbolo
            assert consumidos == len(lexema)
            assert categoria == Categoria.OPERADOR_ARITMETICO

    def test_operador_comparacion(self, afd):
        simbolos = ['==', '!=', '===', '!==', '<', '>', '<=', '>=']
        for simbolo in simbolos:
            valido, lexema, consumidos, categoria = afd.analizar(simbolo, 0)
            assert valido is True
            assert lexema == simbolo
            assert consumidos == len(lexema)
            assert categoria == Categoria.OPERADOR_COMPARACION

    def test_operador_logico(self, afd):
        simbolos = ['&&', '||', '!']
        for simbolo in simbolos:
            valido, lexema, consumidos, categoria = afd.analizar(simbolo, 0)
            assert valido is True
            assert lexema == simbolo
            assert consumidos == len(lexema)
            assert categoria == Categoria.OPERADOR_LOGICO

    def test_operador_asignacion(self, afd):
        simbolos = ['=', '+=', '-=', '*=', '/=', '%=', '**=', '&&=', '||=', '??=']
        for simbolo in simbolos:
            valido, lexema, consumidos, categoria = afd.analizar(simbolo, 0)
            assert valido is True
            assert lexema == simbolo
            assert consumidos == len(lexema)
            assert categoria == Categoria.OPERADOR_ASIGNACION

    def test_operador_incremento(self, afd):
        simbolos = ['++', '--']
        for simbolo in simbolos:
            valido, lexema, consumidos, categoria = afd.analizar(simbolo, 0)
            assert valido is True
            assert lexema == simbolo
            assert consumidos == len(lexema)
            if simbolo == '++':
                assert categoria == Categoria.OPERADOR_INCREMENTO
            else:
                assert categoria == Categoria.OPERADOR_DECREMENTO

    def test_operador_acceso(self, afd):
        simbolos = ['.', '?.', '?.[', '?.[]']
        for simbolo in simbolos:
            valido, lexema, consumidos, categoria = afd.analizar(simbolo, 0)
            assert valido is True
            assert lexema == simbolo
            assert consumidos == len(lexema)
            assert categoria == Categoria.OPERADOR_ACCESO or categoria == Categoria.PUNTO

    def test_operador_typescript(self, afd):
        simbolos = ['?', '??', '|', '&', '<', '>', '${', '}', 'extends', 'in', 'readonly', 'unique', 'override', 'keyof', 'infer', 'as', 'satisfies', 'asserts', 'const', 'let', 'var', 'import', 'export', 'default', 'from', 'of', 'with', 'yield']
        for simbolo in simbolos:
            valido, lexema, consumidos, categoria = afd.analizar(simbolo, 0)
            assert valido is True
            assert lexema == simbolo
            assert consumidos == len(lexema)
            assert categoria == Categoria.OPERADOR_TYPESCRIPT

    def test_simbolo_basico(self, afd):
        simbolos = ['(', ')', '{', '}', '[', ']', ';', ',', '.']
        categorias = [Categoria.PARENTESIS_IZQ, Categoria.PARENTESIS_DER, Categoria.LLAVE_IZQ, Categoria.LLAVE_DER, Categoria.CORCHETE_IZQ, Categoria.CORCHETE_DER, Categoria.PUNTO_Y_COMA, Categoria.COMA, Categoria.PUNTO]
        for simbolo, cat_esperada in zip(simbolos, categorias):
            valido, lexema, consumidos, categoria = afd.analizar(simbolo, 0)
            assert valido is True
            assert lexema == simbolo
            assert consumidos == len(lexema)
            assert categoria == cat_esperada

    def test_simbolo_no_valido(self, afd):
        simbolos = ['a', '@', '###', '!=!', '']
        for simbolo in simbolos:
            valido, lexema, consumidos, categoria = afd.analizar(simbolo, 0)
            assert valido is False
            assert lexema == ''
            assert consumidos == 0
            assert categoria is None

    def test_cadena_vacia(self, afd):
        valido, lexema, consumidos, cat = afd.analizar('', 0)
        assert valido is False
        assert lexema == ''
        assert consumidos == 0
        assert cat is None

    def test_simbolo_en_medio(self, afd):
        texto = 'abc+def'
        valido, lexema, consumidos, cat = afd.analizar(texto, 3)
        assert valido is True
        assert lexema == '+'
        assert consumidos == 1
        assert cat == Categoria.OPERADOR_ARITMETICO

    def test_simbolo_compuesto_incompleto(self, afd):
        texto = '='
        valido, lexema, consumidos, cat = afd.analizar(texto, 0)
        assert valido is True
        assert lexema == '='
        assert consumidos == 1
        assert cat == Categoria.OPERADOR_ASIGNACION

    def test_simbolo_compuesto_completo(self, afd):
        texto = '=='
        valido, lexema, consumidos, cat = afd.analizar(texto, 0)
        assert valido is True
        assert lexema == '=='
        assert consumidos == 2
        assert cat == Categoria.OPERADOR_COMPARACION

def test_operador_aritmetico(afd):
    """Prueba operadores aritméticos."""
    valido, lexema, consumidos, categoria = afd.analizar('+', 0)
    assert valido == True
    assert lexema == '+'
    assert consumidos == 1
    assert categoria == Categoria.OPERADOR_ARITMETICO

def test_operador_comparacion(afd):
    """Prueba operadores de comparación."""
    valido, lexema, consumidos, categoria = afd.analizar('==', 0)
    assert valido == True
    assert lexema == '=='
    assert consumidos == 2
    assert categoria == Categoria.OPERADOR_COMPARACION

def test_operador_logico(afd):
    """Prueba operadores lógicos."""
    valido, lexema, consumidos, categoria = afd.analizar('&&', 0)
    assert valido == True
    assert lexema == '&&'
    assert consumidos == 2
    assert categoria == Categoria.OPERADOR_LOGICO

def test_operador_asignacion(afd):
    """Prueba operadores de asignación."""
    valido, lexema, consumidos, categoria = afd.analizar('+=', 0)
    assert valido == True
    assert lexema == '+='
    assert consumidos == 2
    assert categoria == Categoria.OPERADOR_ASIGNACION

def test_operador_incremento(afd):
    """Prueba operadores de incremento."""
    valido, lexema, consumidos, categoria = afd.analizar('++', 0)
    assert valido == True
    assert lexema == '++'
    assert consumidos == 2
    assert categoria == Categoria.OPERADOR_INCREMENTO

def test_operador_acceso(afd):
    """Prueba operadores de acceso."""
    valido, lexema, consumidos, categoria = afd.analizar('?.', 0)
    assert valido == True
    assert lexema == '?.'
    assert consumidos == 2
    assert categoria == Categoria.OPERADOR_ACCESO

def test_operador_typescript(afd):
    """Prueba operadores de TypeScript."""
    valido, lexema, consumidos, categoria = afd.analizar('??', 0)
    assert valido == True
    assert lexema == '??'
    assert consumidos == 2
    assert categoria == Categoria.OPERADOR_TYPESCRIPT

def test_simbolo_basico(afd):
    """Prueba símbolos básicos."""
    valido, lexema, consumidos, categoria = afd.analizar('(', 0)
    assert valido == True
    assert lexema == '('
    assert consumidos == 1
    assert categoria == Categoria.PARENTESIS_IZQ

def test_simbolo_no_valido(afd):
    """Prueba símbolos no válidos."""
    valido, lexema, consumidos, categoria = afd.analizar('a', 0)
    assert valido == False
    assert lexema == ''
    assert consumidos == 0
    assert categoria is None 