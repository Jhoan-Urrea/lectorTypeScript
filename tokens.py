#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Definición de categorías de tokens y clase Token para el análisis léxico de TypeScript.
"""

from enum import Enum, auto

class Categoria(Enum):
    # Identificadores y literales
    IDENTIFICADOR = auto()
    NUMERO_NATURAL = auto()
    NUMERO_REAL = auto()
    CADENA = auto()
    
    # Palabras reservadas básicas
    PALABRA_RESERVADA = auto()
    
    # Tipos de TypeScript
    TIPO_PRIMITIVO = auto()
    TIPO_INTERFACE = auto()
    TIPO_TYPE = auto()
    TIPO_ENUM = auto()
    TIPO_KEYOF = auto()
    TIPO_INFER = auto()
    TIPO_UNION = auto()          # Para tipos union (|)
    TIPO_INTERSECTION = auto()   # Para tipos intersection (&)
    TIPO_GENERIC = auto()        # Para tipos genéricos (<T>)
    TIPO_TEMPLATE = auto()       # Para template literal types
    
    # Operadores
    OPERADOR_ARITMETICO = auto()
    OPERADOR_COMPARACION = auto()
    OPERADOR_LOGICO = auto()
    OPERADOR_ASIGNACION = auto()
    OPERADOR_INCREMENTO = auto()
    OPERADOR_DECREMENTO = auto()
    OPERADOR_ACCESO = auto()
    OPERADOR_TYPESCRIPT = auto()
    OPERADOR_UNION = auto()      # |
    OPERADOR_INTERSECTION = auto() # &
    OPERADOR_OPTIONAL = auto()   # ?
    OPERADOR_NON_NULL = auto()   # !
    
    # Símbolos
    PARENTESIS_IZQ = auto()
    PARENTESIS_DER = auto()
    LLAVE_IZQ = auto()
    LLAVE_DER = auto()
    CORCHETE_IZQ = auto()
    CORCHETE_DER = auto()
    PUNTO_Y_COMA = auto()
    COMA = auto()
    PUNTO = auto()
    MENOR_QUE = auto()          # <
    MAYOR_QUE = auto()          # >
    
    # Comentarios
    COMENTARIO_LINEA = auto()
    COMENTARIO_BLOQUE = auto()
    
    # Fin de archivo
    EOF = auto()

class Token:
    def __init__(self, lexema, categoria, fila, columna):
        """
        Inicializa un nuevo token.
        
        Args:
            lexema: El texto del token
            categoria: La categoría del token (usar constantes de la clase Categoria)
            fila: Número de fila donde comienza el token (1-indexado)
            columna: Número de columna donde comienza el token (1-indexado)
        """
        self.lexema = lexema
        self.categoria = categoria
        self.fila = fila
        self.columna = columna
    
    def __str__(self):
        """Representación en string del token."""
        return f"Token({self.lexema}, {self.categoria}, {self.fila}, {self.columna})"
    
    def __repr__(self):
        """Representación en string del token para depuración."""
        return self.__str__()

# Diccionario de palabras reservadas con sus categorías
PALABRAS_RESERVADAS = {
    # Palabras reservadas básicas
    "if": Categoria.PALABRA_RESERVADA,
    "else": Categoria.PALABRA_RESERVADA,
    "while": Categoria.PALABRA_RESERVADA,
    "for": Categoria.PALABRA_RESERVADA,
    "do": Categoria.PALABRA_RESERVADA,
    "switch": Categoria.PALABRA_RESERVADA,
    "case": Categoria.PALABRA_RESERVADA,
    "break": Categoria.PALABRA_RESERVADA,
    "continue": Categoria.PALABRA_RESERVADA,
    "return": Categoria.PALABRA_RESERVADA,
    "function": Categoria.PALABRA_RESERVADA,
    "class": Categoria.PALABRA_RESERVADA,
    "new": Categoria.PALABRA_RESERVADA,
    "this": Categoria.PALABRA_RESERVADA,
    "super": Categoria.PALABRA_RESERVADA,
    "import": Categoria.PALABRA_RESERVADA,
    "export": Categoria.PALABRA_RESERVADA,
    "default": Categoria.PALABRA_RESERVADA,
    "const": Categoria.PALABRA_RESERVADA,
    "let": Categoria.PALABRA_RESERVADA,
    "var": Categoria.PALABRA_RESERVADA,
    "try": Categoria.PALABRA_RESERVADA,
    "catch": Categoria.PALABRA_RESERVADA,
    "finally": Categoria.PALABRA_RESERVADA,
    "throw": Categoria.PALABRA_RESERVADA,
    
    # Tipos primitivos
    "string": Categoria.TIPO_PRIMITIVO,
    "number": Categoria.TIPO_PRIMITIVO,
    "boolean": Categoria.TIPO_PRIMITIVO,
    "symbol": Categoria.TIPO_PRIMITIVO,
    "object": Categoria.TIPO_PRIMITIVO,
    "any": Categoria.TIPO_PRIMITIVO,
    "unknown": Categoria.TIPO_PRIMITIVO,
    "never": Categoria.TIPO_PRIMITIVO,
    "void": Categoria.TIPO_PRIMITIVO,
    "bigint": Categoria.TIPO_PRIMITIVO,
    
    # Tipos especiales
    "interface": Categoria.TIPO_INTERFACE,
    "type": Categoria.TIPO_TYPE,
    "enum": Categoria.TIPO_ENUM,
    "keyof": Categoria.TIPO_KEYOF,
    "infer": Categoria.TIPO_INFER,
    
    # Modificadores de tipo y clase
    "readonly": Categoria.PALABRA_RESERVADA,
    "unique": Categoria.PALABRA_RESERVADA,
    "override": Categoria.PALABRA_RESERVADA,
    "abstract": Categoria.PALABRA_RESERVADA,
    "static": Categoria.PALABRA_RESERVADA,
    "private": Categoria.PALABRA_RESERVADA,
    "protected": Categoria.PALABRA_RESERVADA,
    "public": Categoria.PALABRA_RESERVADA,
    
    # Palabras clave de TypeScript
    "extends": Categoria.PALABRA_RESERVADA,
    "implements": Categoria.PALABRA_RESERVADA,
    "namespace": Categoria.PALABRA_RESERVADA,
    "module": Categoria.PALABRA_RESERVADA,
    "declare": Categoria.PALABRA_RESERVADA,
    "async": Categoria.PALABRA_RESERVADA,
    "await": Categoria.PALABRA_RESERVADA,
    "get": Categoria.PALABRA_RESERVADA,
    "set": Categoria.PALABRA_RESERVADA,
    "in": Categoria.PALABRA_RESERVADA,
    "instanceof": Categoria.PALABRA_RESERVADA,
    "typeof": Categoria.PALABRA_RESERVADA,
    "as": Categoria.PALABRA_RESERVADA,
    "is": Categoria.PALABRA_RESERVADA,
    "satisfies": Categoria.PALABRA_RESERVADA,
    "asserts": Categoria.PALABRA_RESERVADA,
    "constructor": Categoria.PALABRA_RESERVADA,
    "target": Categoria.PALABRA_RESERVADA,
    "value": Categoria.PALABRA_RESERVADA,
    
    # Palabras reservadas adicionales
    "from": Categoria.PALABRA_RESERVADA,
    "of": Categoria.PALABRA_RESERVADA,
    "with": Categoria.PALABRA_RESERVADA,
    "yield": Categoria.PALABRA_RESERVADA,
    
    # Valores literales
    "true": Categoria.PALABRA_RESERVADA,
    "false": Categoria.PALABRA_RESERVADA,
    "null": Categoria.PALABRA_RESERVADA,
    "undefined": Categoria.PALABRA_RESERVADA
} 