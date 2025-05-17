class ComentarioBloqueAFD:
    def __init__(self):
        pass
        
    def analizar(self, texto, pos_inicial):
        """
        Analiza si a partir de la posición inicial hay un comentario de bloque.
        Un comentario de bloque comienza con /* y termina con */.
        
        Args:
            texto: Cadena de texto a analizar
            pos_inicial: Posición desde donde comenzar el análisis
            
        Returns:
            Tupla de (es_valido, lexema, caracteres_consumidos)
        """
        # Estados del autómata:
        # 0: Inicial
        # 1: Después de /
        # 2: Dentro del comentario (después de /*)
        # 3: Posible fin (después de * dentro del comentario)
        # 4: Fin de comentario (después de */)
        
        estado = 0
        lexema = ''
        pos = pos_inicial
        
        while pos < len(texto):
            c = texto[pos]
            
            if estado == 0:  # Estado inicial
                if c == '/':
                    estado = 1
                    lexema += c
                    pos += 1
                else:
                    break
                    
            elif estado == 1:  # Después de /
                if c == '*':
                    estado = 2
                    lexema += c
                    pos += 1
                else:
                    break  # No es un comentario de bloque
                    
            elif estado == 2:  # Dentro del comentario
                if c == '*':
                    estado = 3
                    lexema += c
                    pos += 1
                else:
                    lexema += c
                    pos += 1
                    
            elif estado == 3:  # Posible fin
                if c == '/':
                    estado = 4
                    lexema += c
                    pos += 1
                    break  # Fin del comentario
                elif c == '*':
                    lexema += c
                    pos += 1
                    # Seguimos en estado 3
                else:
                    estado = 2  # Volver a estar dentro del comentario
                    lexema += c
                    pos += 1
        
        # Verificar si terminamos con un comentario válido
        if estado == 4:
            return True, lexema, len(lexema)
        else:
            return False, '', 0

if __name__ == "__main__":
    # Pruebas
    afd = ComentarioBloqueAFD()
    
    pruebas = [
        "/* Este es un comentario de bloque */",
        "/**/",
        "/* Comentario\nmultilinea\n*/",
        "/* Comentario sin cerrar",
        "//Esto es otro tipo",
        ""
    ]
    
    for prueba in pruebas:
        valido, lexema, consumidos = afd.analizar(prueba, 0)
        print(f"Entrada: '{prueba}' -> Válido: {valido}, Lexema: '{lexema}', Caracteres consumidos: {consumidos}") 