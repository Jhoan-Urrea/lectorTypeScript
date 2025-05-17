class CadenaAFD:
    def __init__(self):
        self.comilla_apertura = None # Para almacenar el tipo de comilla que abrió la cadena
        
    def analizar(self, texto, pos_inicial):
        """
        Analiza si a partir de la posición inicial hay una cadena de texto.
        Una cadena comienza con " o ' o ` y termina con la misma comilla, 
        y puede contener secuencias de escape \.
        
        Args:
            texto: Cadena de texto a analizar
            pos_inicial: Posición desde donde comenzar el análisis
            
        Returns:
            Tupla de (es_valido, lexema, caracteres_consumidos)
        """
        # Estados del autómata:
        # 0: Inicial
        # 1: Después de la comilla de apertura
        # 2: Después de una barra invertida (escape)
        # 3: Después de la comilla de cierre (estado final)
        
        estado = 0
        lexema = ''
        pos = pos_inicial
        self.comilla_apertura = None # Reiniciar por si se usa múltiples veces
        
        while pos < len(texto):
            c = texto[pos]
            
            if estado == 0:  # Estado inicial
                if c == '"' or c == "'" or c == "`": # Añadido el acento grave
                    self.comilla_apertura = c # Guardar la comilla de apertura
                    estado = 1
                    lexema += c
                    pos += 1
                else:
                    break  # No empieza con comilla
                    
            elif estado == 1:  # Dentro de la cadena
                if c == self.comilla_apertura: # Usar la comilla de apertura guardada
                    estado = 3  # Comilla de cierre, terminó la cadena
                    lexema += c
                    pos += 1
                    break  # Terminar análisis
                elif c == '\\':
                    estado = 2  # Encontramos un escape
                    lexema += c
                    pos += 1
                else:
                    # Permitir saltos de línea dentro de las cadenas (especialmente para template literals)
                    lexema += c  # Cualquier otro carácter es parte de la cadena
                    pos += 1
                    
            elif estado == 2:  # Después de escape
                # Si el escape es la propia comilla de apertura, una barra invertida,
                # o caracteres como n, t, etc., se añade tal cual.
                # No se interpretan aquí, solo se consumen como dos caracteres (\ y el siguiente).
                lexema += c  # El carácter después del escape siempre se toma literal
                estado = 1  # Volver al estado dentro de la cadena
                pos += 1
        
        # Verificar si terminamos con una cadena válida
        if estado == 3:
            return True, lexema, len(lexema)
        else:
            # Si no se cerró la cadena, y se inició una, es un error no consumido por este AFD
            # Devolvemos False para que el lexer principal lo marque como error si es necesario
            return False, '', 0

if __name__ == "__main__":
    # Pruebas
    afd = CadenaAFD()
    
    pruebas = [
        '"Hola mundo"',          # Comillas dobles
        "'Hola mundo'",          # Comillas simples
        "`Hola mundo`",          # Template literal simple
        '"Cadena con \\"escape\\""', # Escape de comilla doble
        "'Cadena con \\'escape\\''", # Escape de comilla simple
        "`Cadena con \\`escape\\``", # Escape de acento grave
        '"Cadena sin cerrar',    # Prueba de cadena no cerrada,
        "'Cadena sin cerrar",    # Prueba de cadena no cerrada,
        "`Cadena sin cerrar",    # Prueba de cadena no cerrada,
        'No es cadena',
        '"Cadena con\\nSalto"',    # JS string: "Cadena con\nSalto"
        "'Cadena con\\nSalto'",    # JS string: 'Cadena con\nSalto'
        "`Cadena con\\nSalto`",     # JS string: `Cadena con\nSalto`
        """`Cadena con
Salto literal`""",        # JS template string with a literal newline
        '"Cadena\\tTabulador"',
        "'Cadena\\tTabulador'",
        "`Cadena con ${expresion} interpolada`", 
        '"Cadena\\\\Barra"',  # JS string: "Cadena\\Barra"
        "'Cadena\\\\Barra'",  # JS string: 'Cadena\\Barra'
        '''"Mala 'combinación"''', # Unmatched quote type test
        ''''Mala "combinación"''', # Unmatched quote type test
        "`Mala \"comilla doble\" y 'comilla simple'`", 
        '""', # Empty double quoted string
        "''", # Empty single quoted string
        "``", # Empty template string
        ''    # Empty input string for testing
    ]
    
    for prueba in pruebas:
        valido, lexema, consumidos = afd.analizar(prueba, 0)
        print(f"Entrada: {repr(prueba)} -> Válido: {valido}, Lexema: {repr(lexema)}, Caracteres consumidos: {consumidos}") 