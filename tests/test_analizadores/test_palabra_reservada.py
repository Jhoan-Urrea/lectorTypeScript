#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pruebas para el analizador de palabras reservadas.
"""

import sys
import os
import pytest

# Añadir la raíz del proyecto al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from analizadores.palabra_reservada import PalabraReservadaAFD
from tokens import PALABRAS_RESERVADAS, Categoria

@pytest.fixture
def afd():
    return PalabraReservadaAFD()

class TestPalabraReservadaAFD:
    def test_palabras_reservadas_aisladas_o_con_delimitador(self, afd):
        # Palabras reservadas que están solas o seguidas de un delimitador no alfanumérico
        palabras_reservadas = list(PALABRAS_RESERVADAS.keys())
        casos = palabras_reservadas + [pr + "(" for pr in palabras_reservadas if len(pr) > 1] + [pr + " " for pr in palabras_reservadas if len(pr) > 1]
        
        for caso in casos:
            valido, lexema, consumidos, categoria = afd.analizar(caso, 0)
            assert valido, f"'{caso}' debería ser reconocido como palabra reservada"
            assert lexema in PALABRAS_RESERVADAS, f"'{lexema}' debería estar en PALABRAS_RESERVADAS"
            assert consumidos == len(lexema), f"Debería consumir {len(lexema)} caracteres, consumió {consumidos}"
            assert categoria == PALABRAS_RESERVADAS[lexema], f"La categoría debería ser {PALABRAS_RESERVADAS[lexema]}, fue {categoria}"
    
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
                continue
            
            valido, lexema, consumidos, categoria = afd.analizar(palabra_completa, 0)
            assert not valido, f"'{palabra_completa}' NO debería ser reconocido como palabra reservada"
            assert lexema == "", f"El lexema debería estar vacío, fue '{lexema}'"
            assert consumidos == 0, f"No debería consumir caracteres, consumió {consumidos}"
            assert categoria is None, f"La categoría debería ser None, fue {categoria}"
    
    def test_no_es_palabra_reservada_en_absoluto(self, afd):
        no_reservadas_completamente = [
            "variableXYZ", "funcionABC", "claseDEF",  # No son reservadas y no empiezan con una conocida
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
                continue
            
            valido, lexema, consumidos, categoria = afd.analizar(palabra, 0)
            assert not valido, f"'{palabra}' NO debería ser reconocido como palabra reservada"
            assert lexema == "", f"El lexema debería estar vacío, fue '{lexema}'"
            assert consumidos == 0, f"No debería consumir caracteres, consumió {consumidos}"
            assert categoria is None, f"La categoría debería ser None, fue {categoria}"
    
    def test_palabra_reservada_en_medio_no_debe_reconocer(self, afd):
        # Con la lógica actual de PalabraReservadaAFD, "if" en "123if456" no se reconocerá
        texto = "123if456"
        valido, lexema, consumidos, categoria = afd.analizar(texto, 3)  # Analizar "if456"
        assert not valido, f"'{texto[3:]}' NO debería ser reconocido como palabra reservada"
        assert lexema == "", f"El lexema debería estar vacío, fue '{lexema}'"
        assert consumidos == 0, f"No debería consumir caracteres, consumió {consumidos}"
        assert categoria is None, f"La categoría debería ser None, fue {categoria}"
    
    def test_tipos_primitivos(self, afd):
        tipos_primitivos = ["string", "number", "boolean", "symbol", "object", "any", "unknown", "never", "void"]
        for tipo in tipos_primitivos:
            valido, lexema, consumidos, categoria = afd.analizar(tipo, 0)
            assert valido, f"'{tipo}' debería ser reconocido como tipo primitivo"
            assert lexema == tipo, f"El lexema debería ser '{tipo}', fue '{lexema}'"
            assert consumidos == len(tipo), f"Debería consumir {len(tipo)} caracteres, consumió {consumidos}"
            assert categoria == Categoria.TIPO_PRIMITIVO, f"La categoría debería ser TIPO_PRIMITIVO, fue {categoria}"
    
    def test_tipos_especiales(self, afd):
        tipos_especiales = {
            "interface": Categoria.TIPO_INTERFACE,
            "type": Categoria.TIPO_TYPE,
            "enum": Categoria.TIPO_ENUM,
            "keyof": Categoria.TIPO_KEYOF,
            "infer": Categoria.TIPO_INFER
        }
        for tipo, categoria_esperada in tipos_especiales.items():
            valido, lexema, consumidos, categoria = afd.analizar(tipo, 0)
            assert valido, f"'{tipo}' debería ser reconocido como tipo especial"
            assert lexema == tipo, f"El lexema debería ser '{tipo}', fue '{lexema}'"
            assert consumidos == len(tipo), f"Debería consumir {len(tipo)} caracteres, consumió {consumidos}"
            assert categoria == categoria_esperada, f"La categoría debería ser {categoria_esperada}, fue {categoria}"

def test_palabra_reservada_basica(afd):
    """Prueba palabras reservadas básicas."""
    valido, lexema, consumidos, categoria = afd.analizar('if', 0)
    assert valido == True
    assert lexema == 'if'
    assert consumidos == 2
    assert categoria == Categoria.PALABRA_RESERVADA

def test_palabra_reservada_tipo_primitivo(afd):
    """Prueba palabras reservadas que son tipos primitivos."""
    valido, lexema, consumidos, categoria = afd.analizar('string', 0)
    assert valido == True
    assert lexema == 'string'
    assert consumidos == 6
    assert categoria == Categoria.TIPO_PRIMITIVO

def test_palabra_reservada_tipo_especial(afd):
    """Prueba palabras reservadas que son tipos especiales."""
    valido, lexema, consumidos, categoria = afd.analizar('interface', 0)
    assert valido == True
    assert lexema == 'interface'
    assert consumidos == 9
    assert categoria == Categoria.TIPO_INTERFACE

def test_palabra_reservada_nueva(afd):
    """Prueba las nuevas palabras reservadas agregadas."""
    for palabra in ['from', 'of', 'with', 'yield']:
        valido, lexema, consumidos, categoria = afd.analizar(palabra, 0)
        assert valido == True
        assert lexema == palabra
        assert consumidos == len(palabra)
        assert categoria == Categoria.PALABRA_RESERVADA

def test_palabra_reservada_seguida_de_identificador(afd):
    """Prueba que una palabra reservada seguida de caracteres de identificador no es reconocida."""
    valido, lexema, consumidos, categoria = afd.analizar('ifx', 0)
    assert valido == False

def test_palabra_reservada_en_posicion_distinta(afd):
    """Prueba una palabra reservada en una posición distinta del texto."""
    texto = 'let if = 5;'
    valido, lexema, consumidos, categoria = afd.analizar(texto, 4)
    assert valido == True
    assert lexema == 'if'
    assert consumidos == 2
    assert categoria == Categoria.PALABRA_RESERVADA 