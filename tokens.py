#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Definición de categorías de tokens y clase Token para el análisis léxico.
"""

# Categorías de tokens en JavaScript
class Categoria:
    IDENTIFICADOR = "IDENTIFICADOR"
    NUMERO_NATURAL = "NUMERO_NATURAL"
    NUMERO_REAL = "NUMERO_REAL"
    CADENA = "CADENA"
    PALABRA_RESERVADA = "PALABRA_RESERVADA"
    COMENTARIO_LINEA = "COMENTARIO_LINEA"
    COMENTARIO_BLOQUE = "COMENTARIO_BLOQUE"
    
    # Operadores
    OPERADOR_ARITMETICO = "OPERADOR_ARITMETICO"
    OPERADOR_COMPARACION = "OPERADOR_COMPARACION"
    OPERADOR_LOGICO = "OPERADOR_LOGICO"
    OPERADOR_ASIGNACION = "OPERADOR_ASIGNACION"
    OPERADOR_INCREMENTO = "OPERADOR_INCREMENTO"
    OPERADOR_DECREMENTO = "OPERADOR_DECREMENTO"
    OPERADOR_ACCESO = "OPERADOR_ACCESO"  # Nueva categoría para el punto (.)
    SIGNO_INTERROGACION = "SIGNO_INTERROGACION" # Para el ? (operador ternario)
    OPERADOR_OPTIONAL_CHAINING = "OPERADOR_OPTIONAL_CHAINING" # Para ?. 
    OPERADOR_NULISH_COALESCING = "OPERADOR_NULISH_COALESCING" # Para ??
    
    # Delimitadores
    PARENTESIS_APERTURA = "PARENTESIS_APERTURA"
    PARENTESIS_CIERRE = "PARENTESIS_CIERRE"
    LLAVE_APERTURA = "LLAVE_APERTURA"
    LLAVE_CIERRE = "LLAVE_CIERRE"
    CORCHETE_APERTURA = "CORCHETE_APERTURA"
    CORCHETE_CIERRE = "CORCHETE_CIERRE"
    DOS_PUNTOS = "DOS_PUNTOS"
    
    # Otros
    TERMINAL = "TERMINAL"           # Punto y coma (;)
    SEPARADOR = "SEPARADOR"         # Coma (,)
    
    # Errores
    ERROR = "ERROR"

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

# Palabras reservadas de JavaScript para analizador
PALABRAS_RESERVADAS = [
    # Declaraciones 
    "var", "let", "const", "function", "class",
    
    # Control de flujo
    "if", "else", "switch", "case", "default", "break", 
    "continue", "return", "while", "for", "do",
    
    # Operadores/Palabras clave
    "new", "this", "super", "delete", "typeof", "instanceof",
    "void", "yield", "await", "in", "of",
    
    # Valores literales
    "true", "false", "null", "undefined", 
    
    # Manejo de excepciones
    "try", "catch", "finally", "throw"
] 