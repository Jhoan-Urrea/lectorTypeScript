import pytest
import sys
import os

# Añadir la raíz del proyecto al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from analizadores.comentario_bloque import ComentarioBloqueAFD

@pytest.fixture
def afd():
    return ComentarioBloqueAFD()

class TestComentarioBloqueAFD:
    def test_comentario_bloque_simple(self, afd):
        texto = '/* Este es un comentario de bloque */'
        valido, lexema, consumidos = afd.analizar(texto, 0)
        assert valido is True
        assert lexema == texto
        assert consumidos == len(lexema)

    def test_comentario_bloque_vacio(self, afd):
        texto = '/**/'
        valido, lexema, consumidos = afd.analizar(texto, 0)
        assert valido is True
        assert lexema == texto
        assert consumidos == len(lexema)

    def test_comentario_bloque_multilinea(self, afd):
        texto = '/* Comentario\nmultilinea\n*/'
        valido, lexema, consumidos = afd.analizar(texto, 0)
        assert valido is True
        assert lexema == texto
        assert consumidos == len(lexema)

    def test_comentario_bloque_sin_cerrar(self, afd):
        texto = '/* Comentario sin cerrar'
        valido, lexema, consumidos = afd.analizar(texto, 0)
        assert valido is False
        assert lexema == ''
        assert consumidos == 0

    def test_no_es_comentario_bloque(self, afd):
        texto = '// Esto no es bloque'
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

    def test_comentario_bloque_asteriscos(self, afd):
        texto = '/* **** */'
        valido, lexema, consumidos = afd.analizar(texto, 0)
        assert valido is True
        assert lexema == texto
        assert consumidos == len(lexema)

    def test_comentario_bloque_con_otros_simbolos(self, afd):
        texto = '/* { [ ( ) ] } */'
        valido, lexema, consumidos = afd.analizar(texto, 0)
        assert valido is True
        assert lexema == texto
        assert consumidos == len(lexema)

    def test_comentario_bloque_anidado_no_valido(self, afd):
        texto = '/* comentario /* anidado */ fin */'
        # Solo debe reconocer hasta el primer cierre */
        valido, lexema, consumidos = afd.analizar(texto, 0)
        # El analizador actual reconoce hasta el primer */
        esperado = '/* comentario /* anidado */'
        assert valido is True
        assert lexema == esperado
        assert consumidos == len(esperado)

    def test_comentario_bloque_con_espacios(self, afd):
        texto = '/*    */'
        valido, lexema, consumidos = afd.analizar(texto, 0)
        assert valido is True
        assert lexema == texto
        assert consumidos == len(lexema)

    def test_comentario_bloque_con_unicode(self, afd):
        texto = '/* Comentario con ñ y áéíóú */'
        valido, lexema, consumidos = afd.analizar(texto, 0)
        assert valido is True
        assert lexema == texto
        assert consumidos == len(lexema)

    def test_comentario_bloque_con_espacios_antes(self, afd):
        texto = '   /* Comentario con espacios antes */'
        valido, lexema, consumidos = afd.analizar(texto, 0)
        assert valido is False  # No debe reconocer si hay espacios antes
        assert lexema == ''
        assert consumidos == 0

    def test_comentario_bloque_muy_largo(self, afd):
        texto = '/* ' + 'a' * 1000 + ' */'
        valido, lexema, consumidos = afd.analizar(texto, 0)
        assert valido is True
        assert lexema == texto
        assert consumidos == len(lexema)

    def test_comentario_bloque_con_caracteres_especiales(self, afd):
        texto = '/* !@#$%^&*()_+-=[]{}|;:,.<>? */'
        valido, lexema, consumidos = afd.analizar(texto, 0)
        assert valido is True
        assert lexema == texto
        assert consumidos == len(lexema)

    def test_comentario_bloque_jsdoc(self, afd):
        texto = '''/**
 * Sistema de Gestión de Tareas Avanzado
 * 
 * Esta función permite:
 * - Añadir tareas con prioridad, categoría y fecha límite
 * - Marcar tareas como completadas
 * - Filtrar tareas por diferentes criterios
 * - Estadísticas de productividad
 * - Persistencia en localStorage
 * - Notificaciones de tareas próximas
 */'''
        valido, lexema, consumidos = afd.analizar(texto, 0)
        assert valido is True
        assert lexema == texto
        assert consumidos == len(lexema)

    def test_comentario_bloque_con_salto_linea_windows(self, afd):
        texto = '/* Comentario\r\ncon salto de línea Windows */'
        valido, lexema, consumidos = afd.analizar(texto, 0)
        assert valido is True
        assert lexema == texto
        assert consumidos == len(lexema) 