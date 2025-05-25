import pytest
import sys
import os

# Añadir la raíz del proyecto al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) )

from analizadores.comentario_linea import ComentarioLineaAFD
from analizadores.comentario_bloque import ComentarioBloqueAFD
from tokens import Categoria, Token

# Tests para comentarios de línea
class TestComentarioLineaAFD:
    @pytest.fixture
    def afd(self):
        return ComentarioLineaAFD()

    def test_comentario_linea_simple(self, afd):
        resultado = afd.analizar('// Esto es un comentario')
        assert resultado is not None
        assert resultado.categoria == Categoria.COMENTARIO_LINEA

    def test_comentario_linea_vacio(self, afd):
        resultado = afd.analizar('//')
        assert resultado is not None
        assert resultado.categoria == Categoria.COMENTARIO_LINEA

    def test_comentario_linea_unicode(self, afd):
        resultado = afd.analizar('// áéíóú')
        assert resultado is not None
        assert resultado.categoria == Categoria.COMENTARIO_LINEA

    def test_comentario_linea_todo(self, afd):
        resultado = afd.analizar('// TODO: revisar esto')
        assert resultado is not None
        assert resultado.categoria == Categoria.COMENTARIO_LINEA

    def test_comentario_linea_ts_ignore(self, afd):
        resultado = afd.analizar('// @ts-ignore')
        assert resultado is not None
        assert resultado.categoria == Categoria.COMENTARIO_LINEA

    def test_no_es_comentario_linea(self, afd):
        resultado = afd.analizar('let x = 5;')
        assert resultado is None

# Tests para comentarios de bloque
class TestComentarioBloqueAFD:
    @pytest.fixture
    def afd(self):
        return ComentarioBloqueAFD()

    def test_comentario_bloque_simple(self, afd):
        resultado = afd.analizar('/* Esto es un comentario */')
        assert resultado is not None
        assert resultado.categoria == Categoria.COMENTARIO_BLOQUE

    def test_comentario_bloque_multilinea(self, afd):
        resultado = afd.analizar('/* Línea 1\nLínea 2 */')
        assert resultado is not None
        assert resultado.categoria == Categoria.COMENTARIO_BLOQUE

    def test_comentario_bloque_jsdoc(self, afd):
        resultado = afd.analizar('/** Documentación */')
        assert resultado is not None
        assert resultado.categoria == Categoria.COMENTARIO_BLOQUE

    def test_comentario_bloque_unicode(self, afd):
        resultado = afd.analizar('/* áéíóú */')
        assert resultado is not None
        assert resultado.categoria == Categoria.COMENTARIO_BLOQUE

    def test_comentario_bloque_sin_cerrar(self, afd):
        resultado = afd.analizar('/* sin cerrar')
        assert resultado is None

    def test_no_es_comentario_bloque(self, afd):
        resultado = afd.analizar('let x = 5;')
        assert resultado is None

    def test_comentario_linea_no_al_inicio(self, afd):
        texto = 'let x = 5; // comentario'
        valido, lexema, consumidos, categoria = afd.analizar(texto, 11)
        esperado = '// comentario'
        assert valido is True
        assert lexema == esperado
        assert consumidos == len(esperado)
        assert categoria == Categoria.COMENTARIO_LINEA 