import pytest
import sys
import os

# Añadir la raíz del proyecto al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from analizadores.identificador import IdentificadorAFD

@pytest.fixture
def afd():
    return IdentificadorAFD()

class TestIdentificadorAFD:
    def test_identificador_simple(self, afd):
        """Prueba un identificador simple"""
        valido, lexema, consumidos, _ = afd.analizar('variable', 0)
        assert valido == True
        assert lexema == 'variable'
        assert consumidos == len(lexema)

    def test_identificador_con_guion_bajo(self, afd):
        """Prueba un identificador con guion bajo"""
        valido, lexema, consumidos, _ = afd.analizar('mi_variable', 0)
        assert valido == True
        assert lexema == 'mi_variable'
        assert consumidos == len(lexema)

    def test_identificador_con_dolar(self, afd):
        """Prueba un identificador con símbolo de dólar"""
        valido, lexema, consumidos, _ = afd.analizar('$variable', 0)
        assert valido == True
        assert lexema == '$variable'
        assert consumidos == len(lexema)

    def test_identificador_con_numeros(self, afd):
        """Prueba un identificador con números"""
        valido, lexema, consumidos, _ = afd.analizar('variable123', 0)
        assert valido == True
        assert lexema == 'variable123'
        assert consumidos == len(lexema)

    def test_identificador_con_mayusculas(self, afd):
        """Prueba un identificador con mayúsculas"""
        valido, lexema, consumidos, _ = afd.analizar('Variable', 0)
        assert valido == True
        assert lexema == 'Variable'
        assert consumidos == len(lexema)

    def test_identificador_con_multiple_palabras(self, afd):
        """Prueba un identificador con múltiples palabras"""
        valido, lexema, consumidos, _ = afd.analizar('miVariableLarga', 0)
        assert valido == True
        assert lexema == 'miVariableLarga'
        assert consumidos == len(lexema)

    def test_identificador_con_guion_bajo_y_numeros(self, afd):
        """Prueba un identificador con guion bajo y números"""
        valido, lexema, consumidos, _ = afd.analizar('variable_123', 0)
        assert valido == True
        assert lexema == 'variable_123'
        assert consumidos == len(lexema)

    def test_identificador_con_dolar_y_numeros(self, afd):
        """Prueba un identificador con símbolo de dólar y números"""
        valido, lexema, consumidos, _ = afd.analizar('$123', 0)
        assert valido == True
        assert lexema == '$123'
        assert consumidos == len(lexema)

    def test_identificador_con_caracteres_especiales(self, afd):
        """Prueba un identificador con caracteres especiales válidos"""
        valido, lexema, consumidos, _ = afd.analizar('_$variable_$123', 0)
        assert valido == True
        assert lexema == '_$variable_$123'
        assert consumidos == len(lexema)

    def test_identificador_invalido_comienza_con_numero(self, afd):
        """Prueba un identificador que comienza con número (inválido)"""
        valido, lexema, consumidos, _ = afd.analizar('123variable', 0)
        assert valido == False
        assert lexema == ''
        assert consumidos == 0

    def test_identificador_invalido_con_caracteres_especiales(self, afd):
        """Prueba un identificador con caracteres especiales inválidos"""
        valido, lexema, consumidos, _ = afd.analizar('variable@123', 0)
        assert valido == False
        assert lexema == ''
        assert consumidos == 0

    def test_identificador_con_unicode(self, afd):
        """Prueba un identificador con caracteres Unicode"""
        valido, lexema, consumidos, _ = afd.analizar('variáble', 0)
        assert valido == True
        assert lexema == 'variáble'
        assert consumidos == len(lexema)

    def test_identificador_con_espacios(self, afd):
        """Prueba un identificador con espacios (debe fallar)"""
        valido, lexema, consumidos, _ = afd.analizar('mi variable', 0)
        assert valido == False
        assert lexema == ''
        assert consumidos == 0

    def test_identificador_con_palabra_reservada(self, afd):
        """Prueba un identificador que es una palabra reservada"""
        valido, lexema, consumidos, _ = afd.analizar('let', 0)
        assert valido == False
        assert lexema == ''
        assert consumidos == 0

    def test_identificador_unicode_inicio(self, afd):
        """Prueba un identificador que comienza con Unicode válido"""
        valido, lexema, consumidos, _ = afd.analizar('ávariable', 0)
        assert valido == True
        assert lexema == 'ávariable'
        assert consumidos == len('ávariable')

    def test_identificador_solo_guion_bajo(self, afd):
        """Prueba un identificador que es solo un guion bajo"""
        valido, lexema, consumidos, _ = afd.analizar('_', 0)
        assert valido == True
        assert lexema == '_'
        assert consumidos == 1

    def test_identificador_solo_dolar(self, afd):
        """Prueba un identificador que es solo un signo de dólar"""
        valido, lexema, consumidos, _ = afd.analizar('$', 0)
        assert valido == True
        assert lexema == '$'
        assert consumidos == 1

    def test_identificador_palabra_reservada_mayuscula(self, afd):
        """Prueba un identificador que es una palabra reservada pero con mayúsculas"""
        valido, lexema, consumidos, _ = afd.analizar('Class', 0)
        assert valido == True
        assert lexema == 'Class'
        assert consumidos == len('Class')

    def test_identificador_en_posicion_distinta(self, afd):
        """Prueba un identificador en una posición distinta del texto (ignorando espacios en blanco)"""
        texto = 'let variable = 5;'
        valido, lexema, consumidos, _ = afd.analizar(texto, 4)
        assert valido == True
        assert lexema == 'variable'
        assert consumidos == len('variable') 