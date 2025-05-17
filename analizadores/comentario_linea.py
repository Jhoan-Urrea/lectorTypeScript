class ComentarioLineaAFD:
    def __init__(self):
        pass
        
    def analizar(self, texto, pos_inicial):
        """
        Analiza si a partir de la posición inicial hay un comentario de línea.
        Un comentario de línea comienza con // y termina al final de la línea.
        
        Args:
            texto: Cadena de texto a analizar
            pos_inicial: Posición desde donde comenzar el análisis
            
        Returns:
            Tupla de (es_valido, lexema, caracteres_consumidos)
        """
        if pos_inicial + 1 >= len(texto):
            return False, '', 0
            
        # Verificar si comienza con //
        if texto[pos_inicial:pos_inicial+2] != '//':
            return False, '', 0
            
        # Es un comentario de línea, consumir hasta el final de la línea
        pos = pos_inicial + 2
        lexema = '//'
        
        while pos < len(texto) and texto[pos] != '\n':
            lexema += texto[pos]
            pos += 1
            
        return True, lexema, len(lexema)

if __name__ == "__main__":
    # Pruebas
    afd = ComentarioLineaAFD()
    
    pruebas = [
        "// Este es un comentario",
        "//",
        "/ No es comentario",
        "/* Esto es otro tipo */",
        ""
    ]
    
    for prueba in pruebas:
        valido, lexema, consumidos = afd.analizar(prueba, 0)
        print(f"Entrada: '{prueba}' -> Válido: {valido}, Lexema: '{lexema}', Caracteres consumidos: {consumidos}") 