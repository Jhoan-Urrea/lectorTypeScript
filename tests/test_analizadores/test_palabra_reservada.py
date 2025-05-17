import pytest
import sys
import os

# Añadir la raíz del proyecto al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from analizadores.palabra_reservada import PalabraReservadaAFD
from tokens import PALABRAS_RESERVADAS

@pytest.fixture
def afd():
    return PalabraReservadaAFD()

class TestPalabraReservadaAFD:
    def test_palabras_reservadas_aisladas_o_con_delimitador(self, afd):
        # Palabras reservadas que están solas o seguidas de un delimitador no alfanumérico
        casos = PALABRAS_RESERVADAS + [pr + "(" for pr in PALABRAS_RESERVADAS if len(pr) > 1] + [pr + " " for pr in PALABRAS_RESERVADAS if len(pr) > 1]
        for palabra_caso in casos:
            # Extraer la parte que debería ser la palabra reservada
            palabra_reservada_real = ''
            for char_pr in palabra_caso:
                if char_pr.isalnum() or char_pr == '_' or char_pr == '$':
                    palabra_reservada_real += char_pr
                else:
                    break
            
            if palabra_reservada_real not in PALABRAS_RESERVADAS:
                # Esto es un sanity check para la construcción de los casos de prueba
                # print(f"Skipping test case construction for '{palabra_caso}' as '{palabra_reservada_real}' is not in PALABRAS_RESERVADAS")
                continue

            valido, lexema, consumidos = afd.analizar(palabra_caso, 0)
            assert valido is True, f"Se esperaba que '{palabra_reservada_real}' en '{palabra_caso}' fuera reconocida"
            assert lexema == palabra_reservada_real
            assert consumidos == len(palabra_reservada_real)

    def test_palabras_reservadas_como_prefijo_de_identificador(self, afd):
        # Casos como "ifX", donde "if" es reservada pero "ifX" es un identificador.
        # El AFD de PalabraReservada NO debe reconocer "if" aquí.
        casos_prefijo = {
            "ifX": "if",
            "whileTrue": "while",
            "forLoop": "for",
            "newVar": "new",
            "variable": "var", # Suponiendo que var es palabra reservada
            "functionX": "function"
        }
        for palabra_completa, pr_prefijo in casos_prefijo.items():
            if pr_prefijo not in PALABRAS_RESERVADAS:
                 # print(f"Advertencia: El prefijo '{pr_prefijo}' del caso '{palabra_completa}' no es una palabra reservada. Revisar casos.")
                 continue
            
            valido, lexema, consumidos = afd.analizar(palabra_completa, 0)
            assert valido is False, f"Se esperaba que '{pr_prefijo}' en '{palabra_completa}' NO fuera reconocida por PalabraReservadaAFD"
            assert lexema == ''
            assert consumidos == 0

    def test_no_es_palabra_reservada_en_absoluto(self, afd):
        no_reservadas_completamente = [
            "variableXYZ", "funcionABC", "claseDEF",  # No son reservadas y no empiezan con una conocida (asumiendo estas no son PR)
            "xyz", "_if_", "$for$", "test",      # No son reservadas
            "", "123",                            # Casos especiales
            "iff", "truee", "falsee"              # Parecidas pero no iguales
        ]
        for palabra in no_reservadas_completamente:
            # Doble check para asegurar que la cadena de prueba no es ni comienza como una palabra reservada válida
            es_o_comienza_con_reservada = False
            for reservada in PALABRAS_RESERVADAS:
                if palabra == reservada or (palabra.startswith(reservada) and len(palabra) > len(reservada) and (palabra[len(reservada)].isalnum() or palabra[len(reservada)] == '_' or palabra[len(reservada)] == '$')):
                    es_o_comienza_con_reservada = True
                    break
            if es_o_comienza_con_reservada:
                # print(f"Advertencia: '{palabra}' parece ser o comenzar como reservada. Revisar lista `no_reservadas_completamente`.")
                continue

            valido, lexema, consumidos = afd.analizar(palabra, 0)
            assert valido is False, f"Se esperaba que '{palabra}' no fuera reconocida como palabra reservada"
            assert lexema == ''
            assert consumidos == 0

    def test_palabra_reservada_en_medio_no_debe_reconocer(self, afd):
        # Con la lógica actual de PalabraReservadaAFD, "if" en "123if456" no se reconocerá
        # porque está seguido por '4' que es un carácter de identificador.
        texto = "123if456"
        valido, lexema, consumidos = afd.analizar(texto, 3) # Analiza desde "if456"
        assert valido is False, "PalabraReservadaAFD no debería reconocer 'if' si está seguido por otro carácter de identificador como '4'"
        assert lexema == ""
        assert consumidos == 0 