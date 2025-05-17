import pytest
import sys
import os

# Añadir la raíz del proyecto al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from analizadores.comentario_linea import ComentarioLineaAFD

@pytest.fixture
def afd():
    return ComentarioLineaAFD()

class TestComentarioLineaAFD:
    def test_comentario_linea_simple(self, afd):
        texto = '// Este es un comentario'
        valido, lexema, consumidos = afd.analizar(texto, 0)
        assert valido is True
        assert lexema == texto
        assert consumidos == len(lexema)

    def test_comentario_linea_vacio(self, afd):
        texto = '//'
        valido, lexema, consumidos = afd.analizar(texto, 0)
        assert valido is True
        assert lexema == texto
        assert consumidos == len(lexema)

    def test_no_es_comentario_linea(self, afd):
        texto = '/ No es comentario'
        valido, lexema, consumidos = afd.analizar(texto, 0)
        assert valido is False
        assert lexema == ''
        assert consumidos == 0

    def test_comentario_bloque_no_valido(self, afd):
        texto = '/* Esto es otro tipo */'
        valido, lexema, consumidos = afd.analizar(texto, 0)
        assert valido is False
        assert lexema == ''
        assert consumidos == 0

    def test_cadena_vacia(self, afd):
        texto = ''
        valido, lexema, consumidos = afd.analizar(texto, 0)
        assert valido is False
        assert lexema == ''
        assert consumidos == 0

    def test_comentario_linea_simbolos(self, afd):
        texto = '// !@#$%^&*()_+-=[]{}|;:,.<>?/'
        valido, lexema, consumidos = afd.analizar(texto, 0)
        assert valido is True
        assert lexema == texto
        assert consumidos == len(lexema)

    def test_comentario_linea_multilinea(self, afd):
        texto = '// comentario de línea\notra linea'
        valido, lexema, consumidos = afd.analizar(texto, 0)
        esperado = '// comentario de línea'
        assert valido is True
        assert lexema == esperado
        assert consumidos == len(esperado)

    def test_comentario_linea_espacios(self, afd):
        texto = '//    '
        valido, lexema, consumidos = afd.analizar(texto, 0)
        assert valido is True
        assert lexema == texto
        assert consumidos == len(lexema)

    def test_comentario_linea_al_final(self, afd):
        texto = 'codigo // comentario'
        # Solo debe reconocer si empieza en la posición del comentario
        valido, lexema, consumidos = afd.analizar(texto, 7)
        esperado = '// comentario'
        assert valido is True
        assert lexema == esperado
        assert consumidos == len(esperado) 