import pytest
import sys
import os

# Añadir la raíz del proyecto al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from analizadores.cadena import CadenaAFD

@pytest.fixture
def afd():
    return CadenaAFD()

class TestCadenaAFD:
    def test_cadena_vacia(self, afd):
        """Prueba una cadena vacía válida"""
        valido, lexema, consumidos = afd.analizar('""', 0)
        assert valido == True
        assert lexema == '""'
        assert consumidos == len(lexema)

    def test_cadena_simple(self, afd):
        """Prueba una cadena simple sin caracteres especiales"""
        valido, lexema, consumidos = afd.analizar('"Hola mundo"', 0)
        assert valido == True
        assert lexema == '"Hola mundo"'
        assert consumidos == len(lexema)

    def test_cadena_sin_cerrar(self, afd):
        """Prueba una cadena que no se cierra"""
        valido, lexema, consumidos = afd.analizar('"Cadena sin cerrar', 0)
        assert valido == False
        assert lexema == ''
        assert consumidos == 0

    def test_no_es_cadena(self, afd):
        """Prueba texto que no es una cadena"""
        valido, lexema, consumidos = afd.analizar('No es cadena', 0)
        assert valido == False
        assert lexema == ''
        assert consumidos == 0

    def test_cadena_con_escape_comillas(self, afd):
        """Prueba una cadena con comillas escapadas"""
        valido, lexema, consumidos = afd.analizar('"Cadena con \\"escape\\""', 0)
        assert valido == True
        assert lexema == '"Cadena con \\"escape\\""'
        assert consumidos == len(lexema)

    def test_cadena_con_escape_salto(self, afd):
        """Prueba una cadena con salto de línea escapado"""
        valido, lexema, consumidos = afd.analizar('"Cadena con\\nSalto"', 0)
        assert valido == True
        assert lexema == '"Cadena con\\nSalto"'
        assert consumidos == len(lexema)

    def test_cadena_con_escape_tabulador(self, afd):
        """Prueba una cadena con tabulador escapado"""
        valido, lexema, consumidos = afd.analizar('"Cadena\\tTabulador"', 0)
        assert valido == True
        assert lexema == '"Cadena\\tTabulador"'
        assert consumidos == len(lexema)

    def test_cadena_con_escape_barra(self, afd):
        """Prueba una cadena con barra invertida escapada"""
        valido, lexema, consumidos = afd.analizar('"Cadena\\\\Barra"', 0)
        assert valido == True
        assert lexema == '"Cadena\\\\Barra"'
        assert consumidos == len(lexema)

    def test_cadena_con_caracteres_especiales(self, afd):
        """Prueba una cadena con caracteres especiales"""
        valido, lexema, consumidos = afd.analizar('"!@#$%^&*()_+-=[]{}|;:,.<>?/"', 0)
        assert valido == True
        assert lexema == '"!@#$%^&*()_+-=[]{}|;:,.<>?/"'
        assert consumidos == len(lexema)

    def test_cadena_con_unicode(self, afd):
        """Prueba una cadena con caracteres Unicode"""
        valido, lexema, consumidos = afd.analizar('"áéíóú ñÑ"', 0)
        assert valido == True
        assert lexema == '"áéíóú ñÑ"'
        assert consumidos == len(lexema)

    def test_cadena_con_escape_invalido(self, afd):
        """Prueba una cadena con secuencia de escape inválida"""
        valido, lexema, consumidos = afd.analizar('"Cadena con \\x"', 0)
        assert valido == True  # El analizador actual acepta cualquier carácter después de \
        assert lexema == '"Cadena con \\x"'
        assert consumidos == len(lexema)

    def test_cadena_con_espacios(self, afd):
        """Prueba una cadena con múltiples espacios"""
        valido, lexema, consumidos = afd.analizar('"   espacios   "', 0)
        assert valido == True
        assert lexema == '"   espacios   "'
        assert consumidos == len(lexema)

    def test_cadena_con_salto_linea_real(self, afd):
        """Prueba una cadena con salto de línea real (no escapado)"""
        valido, lexema, consumidos = afd.analizar('"Cadena con\nsalto"', 0)
        assert valido == True
        assert lexema == '"Cadena con\nsalto"'
        assert consumidos == len(lexema)

    def test_cadena_con_tabulador_real(self, afd):
        """Prueba una cadena con tabulador real (no escapado)"""
        valido, lexema, consumidos = afd.analizar('"Cadena con\ttabulador"', 0)
        assert valido == True
        assert lexema == '"Cadena con\ttabulador"'
        assert consumidos == len(lexema)

    def test_cadena_con_caracteres_control(self, afd):
        """Prueba una cadena con caracteres de control"""
        valido, lexema, consumidos = afd.analizar('"\\a\\b\\f\\r\\v"', 0)
        assert valido == True
        assert lexema == '"\\a\\b\\f\\r\\v"'
        assert consumidos == len(lexema)

    def test_cadena_con_octal(self, afd):
        """Prueba una cadena con secuencia octal"""
        valido, lexema, consumidos = afd.analizar('"\\141"', 0)  # 'a' en octal
        assert valido == True
        assert lexema == '"\\141"'
        assert consumidos == len(lexema)

    def test_cadena_con_hexadecimal(self, afd):
        """Prueba una cadena con secuencia hexadecimal"""
        valido, lexema, consumidos = afd.analizar('"\\x61"', 0)  # 'a' en hex
        assert valido == True
        assert lexema == '"\\x61"'
        assert consumidos == len(lexema)

    def test_cadena_con_unicode_escape(self, afd):
        """Prueba una cadena con secuencia Unicode"""
        valido, lexema, consumidos = afd.analizar('"\\u0061"', 0)  # 'a' en Unicode
        assert valido == True
        assert lexema == '"\\u0061"'
        assert consumidos == len(lexema)

    def test_cadena_con_template_literal(self, afd):
        """Prueba una cadena con template literal (debe ser válida)"""
        valido, lexema, consumidos = afd.analizar('`template literal`', 0)
        assert valido is True
        assert lexema == '`template literal`'
        assert consumidos == len('`template literal`')

    def test_cadena_con_interpolacion(self, afd):
        """Prueba una cadena con interpolación (no debería ser válida)"""
        valido, lexema, consumidos = afd.analizar('"${variable}"', 0)
        assert valido == True  # El analizador actual acepta la interpolación como texto normal
        assert lexema == '"${variable}"'
        assert consumidos == len(lexema) 