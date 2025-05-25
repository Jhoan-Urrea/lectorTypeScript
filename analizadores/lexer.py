#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analizador léxico principal para TypeScript.
Orquesta todos los autómatas para analizar el código fuente.
"""

from tokens import Token, Categoria, PALABRAS_RESERVADAS
from analizadores.identificador import IdentificadorAFD
from analizadores.numero_natural import NumeroNaturalAFD
from analizadores.palabra_reservada import PalabraReservadaAFD
from analizadores.numero_real import NumeroRealAFD
from analizadores.simbolo import SimboloAFD
from analizadores.cadena import CadenaAFD
from analizadores.comentario_linea import ComentarioLineaAFD
from analizadores.comentario_bloque import ComentarioBloqueAFD
# TODO: Importar el resto de analizadores a medida que se implementen

class AnalizadorLexico:
    def __init__(self):
        # Inicializar todos los analizadores
        self.analizadores = {
            "identificador": IdentificadorAFD(),
            "numero_natural": NumeroNaturalAFD(),
            "palabra_reservada": PalabraReservadaAFD(),
            "numero_real": NumeroRealAFD(),
            "simbolo": SimboloAFD(),
            "cadena": CadenaAFD(),
            "comentario_linea": ComentarioLineaAFD(),
            "comentario_bloque": ComentarioBloqueAFD(),
            # TODO: Añadir el resto de analizadores
        }
    
    def analizar(self, codigo_fuente):
        """
        Analiza el código fuente completo y devuelve una lista de tokens.
        Ahora procesa el código como un solo string para soportar comentarios de bloque multilínea.
        """
        tokens = []
        errores = []
        
        pos = 0
        num_linea = 1
        columna = 1
        codigo = codigo_fuente
        longitud = len(codigo)
        
        while pos < longitud:
            c = codigo[pos]
            if c == '\n':
                num_linea += 1
                columna = 1
                pos += 1
                continue
            if c.isspace():
                columna += 1
                pos += 1
                continue
            
            mejor_consumo = 0
            mejor_lexema = ""
            mejor_categoria = None
            mejor_linea = num_linea
            mejor_columna = columna
            
            # Probar comentarios de bloque (/* ... */)
            valido, lexema, consumidos = self.analizadores["comentario_bloque"].analizar(codigo, pos)
            if valido and consumidos > mejor_consumo:
                mejor_consumo = consumidos
                mejor_lexema = lexema
                mejor_categoria = Categoria.COMENTARIO_BLOQUE
            
            # Probar comentarios de línea (//)
            valido, lexema, consumidos = self.analizadores["comentario_linea"].analizar(codigo, pos)
            if valido and consumidos > mejor_consumo:
                mejor_consumo = consumidos
                mejor_lexema = lexema
                mejor_categoria = Categoria.COMENTARIO_LINEA
            
            # Probar cadenas (para reconocer texto entre comillas)
            valido, lexema, consumidos = self.analizadores["cadena"].analizar(codigo, pos)
            if valido and consumidos > mejor_consumo:
                mejor_consumo = consumidos
                mejor_lexema = lexema
                mejor_categoria = Categoria.CADENA
            
            # Probar símbolos (operadores, paréntesis, etc.)
            valido, lexema, consumidos = self.analizadores["simbolo"].analizar(codigo, pos)
            if valido and consumidos > mejor_consumo:
                mejor_consumo = consumidos
                mejor_lexema = lexema
                categoria_simbolo = self.analizadores["simbolo"].obtener_categoria(lexema)
                if categoria_simbolo:
                    mejor_categoria = categoria_simbolo
            
            # Probar palabra reservada o tipo
            valido, lexema, consumidos, categoria = self.analizadores["palabra_reservada"].analizar(codigo, pos)
            if valido and consumidos > mejor_consumo:
                mejor_consumo = consumidos
                mejor_lexema = lexema
                mejor_categoria = categoria
            
            # Probar número real (antes que natural para evitar confusión)
            valido, lexema, consumidos = self.analizadores["numero_real"].analizar(codigo, pos)
            if valido and consumidos > mejor_consumo:
                mejor_consumo = consumidos
                mejor_lexema = lexema
                mejor_categoria = Categoria.NUMERO_REAL
            
            # Probar número natural
            valido, lexema, consumidos = self.analizadores["numero_natural"].analizar(codigo, pos)
            if valido and consumidos > mejor_consumo:
                mejor_consumo = consumidos
                mejor_lexema = lexema
                mejor_categoria = Categoria.NUMERO_NATURAL
            
            # Probar identificador
            valido, lexema, consumidos = self.analizadores["identificador"].analizar(codigo, pos)
            if valido and consumidos > mejor_consumo:
                mejor_consumo = consumidos
                mejor_lexema = lexema
                mejor_categoria = Categoria.IDENTIFICADOR
            
            # Si se encontró un token
            if mejor_consumo > 0:
                # Calcular la línea y columna de inicio del token
                lineas_antes = codigo[:pos].split('\n')
                mejor_linea = len(lineas_antes)
                if '\n' in mejor_lexema:
                    mejor_columna = len(lineas_antes[-1]) + 1
                else:
                    mejor_columna = len(lineas_antes[-1]) + 1
                token = Token(mejor_lexema, mejor_categoria, mejor_linea, mejor_columna)
                tokens.append(token)
                # Avanzar posición y actualizar línea/columna
                for i in range(mejor_consumo):
                    if codigo[pos] == '\n':
                        num_linea += 1
                        columna = 1
                    else:
                        columna += 1
                    pos += 1
            else:
                # Error: carácter no reconocido
                token = Token(codigo[pos], Categoria.ERROR, num_linea, columna)
                errores.append(token)
                columna += 1
                pos += 1
        return tokens, errores

if __name__ == "__main__":
    # Prueba básica
    analizador = AnalizadorLexico()
    
    codigo_prueba = """
    // Declaración de tipos en TypeScript
    interface Usuario {
        nombre: string;
        edad: number;
        activo: boolean;
    }
    
    // Declaración de variables con tipos
    let contador: number = 123;
    const PI: number = 3.14159;
    
    // Ejemplo de tipos genéricos
    function procesar<T>(valor: T): T {
        return valor;
    }
    
    // Ejemplo de tipos union
    type ID = string | number;
    
    // Ejemplo de tipos intersection
    type Empleado = Usuario & {
        departamento: string;
        salario: number;
    };
    """
    
    tokens, errores = analizador.analizar(codigo_prueba)
    
    print("=== TOKENS ===")
    for token in tokens:
        print(token)
        
    print("\n=== ERRORES ===")
    for error in errores:
        print(error) 