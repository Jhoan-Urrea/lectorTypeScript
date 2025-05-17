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
    def test_identificador_letra(self, afd):
        identificadores = ['variable', 'x', 'nombreVariable']
        for identificador in identificadores:
            valido, lexema, consumidos = afd.analizar(identificador, 0)
            assert valido is True
            assert lexema == identificador[:10]  # Truncado a 10 caracteres
            assert consumidos == len(lexema)

    def test_identificador_guion_bajo(self, afd):
        identificadores = ['_variable', '_', 'variable_con_guion']
        for identificador in identificadores:
            valido, lexema, consumidos = afd.analizar(identificador, 0)
            assert valido is True
            assert lexema == identificador[:10]
            assert consumidos == len(lexema)

    def test_identificador_dolar(self, afd):
        identificadores = ['$variable', '$', 'variable$con$dolar']
        for identificador in identificadores:
            valido, lexema, consumidos = afd.analizar(identificador, 0)
            assert valido is True
            assert lexema == identificador[:10]
            assert consumidos == len(lexema)

    def test_identificador_con_numeros(self, afd):
        identificadores = ['var1', '1var', 'var123', 'var_123']
        for identificador in identificadores:
            valido, lexema, consumidos = afd.analizar(identificador, 0)
            # Solo debe aceptar si comienza con letra, _ o $
            if identificador[0].isalpha() or identificador[0] in '_$':
                assert valido is True
                assert lexema == identificador[:10]
                assert consumidos == len(lexema)
            else:
                assert valido is False
                assert lexema == ''
                assert consumidos == 0

    def test_longitud_maxima(self, afd):
        # Probar con un identificador que excede la longitud máxima
        identificador_largo = 'a' * 20  # 20 caracteres
        valido, lexema, consumidos = afd.analizar(identificador_largo, 0)
        assert valido is True
        assert len(lexema) == 10  # Debe truncar a la longitud máxima
        assert consumidos == 10

    def test_no_es_identificador(self, afd):
        no_identificadores = ['123', '@variable', '#var']
        for no_identificador in no_identificadores:
            valido, lexema, consumidos = afd.analizar(no_identificador, 0)
            assert valido is False
            assert lexema == ''
            assert consumidos == 0
        # Casos que empiezan bien pero contienen caracteres no válidos después
        casos = ['var@', 'var#', 'var$@', 'var!', 'var%']
        for caso in casos:
            valido, lexema, consumidos = afd.analizar(caso, 0)
            assert valido is True
            # El lexema debe ser la parte válida hasta el primer carácter no permitido o hasta 10 caracteres
            esperado = ''
            for c in caso:
                if c.isalnum() or c == '_' or c == '$':
                    if len(esperado) < 10:
                        esperado += c
                    else:
                        break
                else:
                    break
            assert lexema == esperado
            assert consumidos == len(lexema)

    def test_cadena_vacia(self, afd):
        valido, lexema, consumidos = afd.analizar('', 0)
        assert valido is False
        assert lexema == ''
        assert consumidos == 0

    def test_identificador_en_medio(self, afd):
        texto = '123variable456'
        valido, lexema, consumidos = afd.analizar(texto, 3)
        assert valido is True
        # Solo puede tomar 10 caracteres válidos desde la posición 3
        assert lexema == 'variable45'
        assert consumidos == 10

    def test_caracteres_especiales(self, afd):
        caracteres_especiales = ['var@', 'var#', 'var$@', 'var!', 'var%']
        for identificador in caracteres_especiales:
            valido, lexema, consumidos = afd.analizar(identificador, 0)
            # El lexema debe ser la parte válida hasta el primer carácter no permitido o hasta 10 caracteres
            esperado = ''
            for c in identificador:
                if c.isalnum() or c == '_' or c == '$':
                    if len(esperado) < 10:
                        esperado += c
                    else:
                        break
                else:
                    break
            assert valido is True
            assert lexema == esperado
            assert consumidos == len(lexema) 