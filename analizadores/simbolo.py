class SimboloAFD:
    def __init__(self):
        # Mapear símbolos a categorías
        self.simbolos = {
            # Operadores aritméticos
            '+': 'OPERADOR_ARITMETICO',
            '-': 'OPERADOR_ARITMETICO',
            '*': 'OPERADOR_ARITMETICO',
            '/': 'OPERADOR_ARITMETICO',
            '%': 'OPERADOR_ARITMETICO',
            
            # Operadores de comparación
            '==': 'OPERADOR_COMPARACION',
            '!=': 'OPERADOR_COMPARACION',
            '>': 'OPERADOR_COMPARACION',
            '<': 'OPERADOR_COMPARACION',
            '>=': 'OPERADOR_COMPARACION',
            '<=': 'OPERADOR_COMPARACION',
            
            # Operadores lógicos
            '&&': 'OPERADOR_LOGICO',
            '||': 'OPERADOR_LOGICO',
            '!': 'OPERADOR_LOGICO',
            
            # Operadores de asignación
            '=': 'OPERADOR_ASIGNACION',
            '+=': 'OPERADOR_ASIGNACION',
            '-=': 'OPERADOR_ASIGNACION',
            '*=': 'OPERADOR_ASIGNACION',
            '/=': 'OPERADOR_ASIGNACION',
            '%=': 'OPERADOR_ASIGNACION',
            
            # Operadores de incremento/decremento
            '++': 'OPERADOR_INCREMENTO',
            '--': 'OPERADOR_DECREMENTO',
            
            # Paréntesis
            '(': 'PARENTESIS_APERTURA',
            ')': 'PARENTESIS_CIERRE',
            
            # Llaves
            '{': 'LLAVE_APERTURA',
            '}': 'LLAVE_CIERRE',
            
            # Corchetes y dos puntos
            '[': 'CORCHETE_APERTURA',
            ']': 'CORCHETE_CIERRE',
            ':': 'DOS_PUNTOS',
            
            # Terminal y separador
            ';': 'TERMINAL',
            ',': 'SEPARADOR',
            '.': 'OPERADOR_ACCESO',

            # Operadores con '?'
            '?': 'SIGNO_INTERROGACION',
            '?.': 'OPERADOR_OPTIONAL_CHAINING',
            '??': 'OPERADOR_NULISH_COALESCING'
        }
        
        # Símbolos que podrían ser parte de símbolos más largos
        self.simbolos_compuestos = ['=', '!', '>', '<', '+', '-', '*', '/', '%', '&', '|', '?']
        
    def analizar(self, texto, pos_inicial):
        """
        Analiza si a partir de la posición inicial hay un símbolo reconocible.
        
        Args:
            texto: Cadena de texto a analizar
            pos_inicial: Posición desde donde comenzar el análisis
            
        Returns:
            Tupla de (es_valido, lexema, caracteres_consumidos)
        """
        if pos_inicial >= len(texto):
            return False, '', 0
            
        # Intentar símbolos de 2 caracteres primero
        if pos_inicial + 1 < len(texto):
            simbolo_2char = texto[pos_inicial:pos_inicial+2]
            if simbolo_2char in self.simbolos:
                return True, simbolo_2char, 2
                
        # Si no hay símbolo de 2 caracteres, intentar con 1 carácter
        simbolo_1char = texto[pos_inicial]
        if simbolo_1char in self.simbolos:
            return True, simbolo_1char, 1
            
        # No se encontró un símbolo válido
        return False, '', 0
        
    def obtener_categoria(self, lexema):
        """
        Obtiene la categoría del símbolo.
        
        Args:
            lexema: El símbolo a categorizar
            
        Returns:
            La categoría del símbolo, o None si no es un símbolo válido
        """
        return self.simbolos.get(lexema, None)

if __name__ == "__main__":
    # Pruebas
    afd = SimboloAFD()
    
    pruebas = [
        "+",        # Operador aritmético
        "-",        # Operador aritmético
        "==",       # Operador comparación
        "!=",       # Operador comparación
        "&&",       # Operador lógico
        "||",       # Operador lógico
        "=",        # Operador asignación
        "+=",       # Operador asignación
        "++",       # Operador incremento
        "--",       # Operador decremento
        "(",        # Paréntesis apertura
        ")",        # Paréntesis cierre
        "{",        # Llave apertura
        "}",        # Llave cierre
        ";",        # Terminal
        ",",        # Separador
        "abc",      # No es un símbolo
        ""          # Vacío
    ]
    
    for prueba in pruebas:
        valido, lexema, consumidos = afd.analizar(prueba, 0)
        categoria = afd.obtener_categoria(lexema) if valido else None
        print(f"Entrada: '{prueba}' -> Válido: {valido}, Lexema: '{lexema}', Caracteres consumidos: {consumidos}, Categoría: {categoria}") 