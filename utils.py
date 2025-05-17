#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Funciones auxiliares para el analizador léxico.
"""

def calcular_posicion(texto, pos):
    """
    Calcula la posición (fila, columna) a partir de un índice en el texto.
    
    Args:
        texto: Texto completo
        pos: Índice en el texto
        
    Returns:
        Tupla (fila, columna) donde ambos empiezan en 1
    """
    if pos >= len(texto):
        # Posición fuera del texto
        lineas = texto.split('\n')
        return len(lineas), 1
    
    # Obtener el texto hasta la posición
    subtexto = texto[:pos]
    
    # Contar las líneas
    lineas = subtexto.split('\n')
    
    # La fila es el número de líneas
    fila = len(lineas)
    
    # La columna es la longitud de la última línea + 1
    columna = len(lineas[-1]) + 1
    
    return fila, columna

def es_delimitador(caracter):
    """
    Verifica si un carácter es un delimitador.
    
    Args:
        caracter: Carácter a verificar
        
    Returns:
        True si es delimitador, False si no
    """
    delimitadores = "()[]{},;:"
    return caracter in delimitadores

def es_operador(caracter):
    """
    Verifica si un carácter es un operador.
    
    Args:
        caracter: Carácter a verificar
        
    Returns:
        True si es operador, False si no
    """
    operadores = "+-*/%=<>!&|^~"
    return caracter in operadores

if __name__ == "__main__":
    # Pruebas
    texto = "Hola\nmundo\nde Python"
    
    print(f"Texto: '{texto}'")
    print(f"Posición 0: {calcular_posicion(texto, 0)}")
    print(f"Posición 5: {calcular_posicion(texto, 5)}")
    print(f"Posición 10: {calcular_posicion(texto, 10)}")
    
    print("\nPrueba delimitadores:")
    for c in "(){},;[]":
        print(f"'{c}' es delimitador: {es_delimitador(c)}")
    
    print("\nPrueba operadores:")
    for c in "+-*/=<>!":
        print(f"'{c}' es operador: {es_operador(c)}") 