import sys
import os

# Añadir la raíz del proyecto al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tokens import Categoria

class SimboloAFD:
    def __init__(self):
        # Diccionario de símbolos y sus categorías
        self.simbolos = {
            # Operadores aritméticos
            '+': Categoria.OPERADOR_ARITMETICO,
            '-': Categoria.OPERADOR_ARITMETICO,
            '*': Categoria.OPERADOR_ARITMETICO,
            '/': Categoria.OPERADOR_ARITMETICO,
            '%': Categoria.OPERADOR_ARITMETICO,
            '**': Categoria.OPERADOR_ARITMETICO,
            
            # Operadores de comparación
            '==': Categoria.OPERADOR_COMPARACION,
            '!=': Categoria.OPERADOR_COMPARACION,
            '===': Categoria.OPERADOR_COMPARACION,
            '!==': Categoria.OPERADOR_COMPARACION,
            '<': Categoria.OPERADOR_COMPARACION,
            '>': Categoria.OPERADOR_COMPARACION,
            '<=': Categoria.OPERADOR_COMPARACION,
            '>=': Categoria.OPERADOR_COMPARACION,
            
            # Operadores lógicos
            '&&': Categoria.OPERADOR_LOGICO,
            '||': Categoria.OPERADOR_LOGICO,
            '!': Categoria.OPERADOR_LOGICO,
            
            # Operadores de asignación
            '=': Categoria.OPERADOR_ASIGNACION,
            '+=': Categoria.OPERADOR_ASIGNACION,
            '-=': Categoria.OPERADOR_ASIGNACION,
            '*=': Categoria.OPERADOR_ASIGNACION,
            '/=': Categoria.OPERADOR_ASIGNACION,
            '%=': Categoria.OPERADOR_ASIGNACION,
            '**=': Categoria.OPERADOR_ASIGNACION,
            '&&=': Categoria.OPERADOR_ASIGNACION,
            '||=': Categoria.OPERADOR_ASIGNACION,
            '??=': Categoria.OPERADOR_ASIGNACION,
            
            # Operadores de incremento/decremento
            '++': Categoria.OPERADOR_INCREMENTO,
            '--': Categoria.OPERADOR_DECREMENTO,
            
            # Operadores de acceso
            '.': Categoria.OPERADOR_ACCESO,
            '?.': Categoria.OPERADOR_ACCESO,
            '?.[': Categoria.OPERADOR_ACCESO,
            '?.[]': Categoria.OPERADOR_ACCESO,
            
            # Operadores de TypeScript
            '?': Categoria.OPERADOR_TYPESCRIPT,
            '??': Categoria.OPERADOR_TYPESCRIPT,
            '|': Categoria.OPERADOR_TYPESCRIPT,
            '&': Categoria.OPERADOR_TYPESCRIPT,
            '<': Categoria.OPERADOR_TYPESCRIPT,
            '>': Categoria.OPERADOR_TYPESCRIPT,
            '${': Categoria.OPERADOR_TYPESCRIPT,
            '}': Categoria.OPERADOR_TYPESCRIPT,
            'extends': Categoria.OPERADOR_TYPESCRIPT,
            'in': Categoria.OPERADOR_TYPESCRIPT,
            'readonly': Categoria.OPERADOR_TYPESCRIPT,
            'unique': Categoria.OPERADOR_TYPESCRIPT,
            'override': Categoria.OPERADOR_TYPESCRIPT,
            'keyof': Categoria.OPERADOR_TYPESCRIPT,
            'infer': Categoria.OPERADOR_TYPESCRIPT,
            'as': Categoria.OPERADOR_TYPESCRIPT,
            'satisfies': Categoria.OPERADOR_TYPESCRIPT,
            'asserts': Categoria.OPERADOR_TYPESCRIPT,
            'const': Categoria.OPERADOR_TYPESCRIPT,
            'let': Categoria.OPERADOR_TYPESCRIPT,
            'var': Categoria.OPERADOR_TYPESCRIPT,
            'import': Categoria.OPERADOR_TYPESCRIPT,
            'export': Categoria.OPERADOR_TYPESCRIPT,
            'default': Categoria.OPERADOR_TYPESCRIPT,
            'from': Categoria.OPERADOR_TYPESCRIPT,
            'of': Categoria.OPERADOR_TYPESCRIPT,
            'with': Categoria.OPERADOR_TYPESCRIPT,
            'yield': Categoria.OPERADOR_TYPESCRIPT,
            
            # Símbolos
            '(': Categoria.PARENTESIS_IZQ,
            ')': Categoria.PARENTESIS_DER,
            '{': Categoria.LLAVE_IZQ,
            '}': Categoria.LLAVE_DER,
            '[': Categoria.CORCHETE_IZQ,
            ']': Categoria.CORCHETE_DER,
            ';': Categoria.PUNTO_Y_COMA,
            ',': Categoria.COMA,
            '.': Categoria.PUNTO,
        }
        
    def analizar(self, texto, pos_inicial):
        """
        Verifica si a partir de la posición inicial hay un símbolo válido.
        
        Args:
            texto: Cadena de texto a analizar
            pos_inicial: Posición desde donde comenzar el análisis
            
        Returns:
            Tupla de (es_valido, lexema, caracteres_consumidos, categoria)
        """
        if pos_inicial >= len(texto):
            return False, '', 0, None
            
        # Intentar con símbolos de 3 caracteres
        if pos_inicial + 2 < len(texto):
            simbolo = texto[pos_inicial:pos_inicial+3]
            if simbolo in self.simbolos:
                return True, simbolo, 3, self.simbolos[simbolo]
                
        # Intentar con símbolos de 2 caracteres
        if pos_inicial + 1 < len(texto):
            simbolo = texto[pos_inicial:pos_inicial+2]
            if simbolo in self.simbolos:
                return True, simbolo, 2, self.simbolos[simbolo]
                
        # Intentar con símbolos de 1 carácter
        simbolo = texto[pos_inicial]
        if simbolo in self.simbolos:
            return True, simbolo, 1, self.simbolos[simbolo]
            
        return False, '', 0, None

if __name__ == "__main__":
    # Pruebas
    afd = SimboloAFD()
    
    print("--- Pruebas del main de SimboloAFD ---")
    pruebas = {
        # Operadores aritméticos
        "+": (True, "+", 1, Categoria.OPERADOR_ARITMETICO),
        "-": (True, "-", 1, Categoria.OPERADOR_ARITMETICO),
        "*": (True, "*", 1, Categoria.OPERADOR_ARITMETICO),
        "/": (True, "/", 1, Categoria.OPERADOR_ARITMETICO),
        "%": (True, "%", 1, Categoria.OPERADOR_ARITMETICO),
        "**": (True, "**", 2, Categoria.OPERADOR_ARITMETICO),
        
        # Operadores de comparación
        "==": (True, "==", 2, Categoria.OPERADOR_COMPARACION),
        "!=": (True, "!=", 2, Categoria.OPERADOR_COMPARACION),
        "===": (True, "===", 3, Categoria.OPERADOR_COMPARACION),
        "!==": (True, "!==", 3, Categoria.OPERADOR_COMPARACION),
        "<": (True, "<", 1, Categoria.OPERADOR_COMPARACION),
        ">": (True, ">", 1, Categoria.OPERADOR_COMPARACION),
        "<=": (True, "<=", 2, Categoria.OPERADOR_COMPARACION),
        ">=": (True, ">=", 2, Categoria.OPERADOR_COMPARACION),
        
        # Operadores lógicos
        "&&": (True, "&&", 2, Categoria.OPERADOR_LOGICO),
        "||": (True, "||", 2, Categoria.OPERADOR_LOGICO),
        "!": (True, "!", 1, Categoria.OPERADOR_LOGICO),
        
        # Operadores de asignación
        "=": (True, "=", 1, Categoria.OPERADOR_ASIGNACION),
        "+=": (True, "+=", 2, Categoria.OPERADOR_ASIGNACION),
        "-=": (True, "-=", 2, Categoria.OPERADOR_ASIGNACION),
        "*=": (True, "*=", 2, Categoria.OPERADOR_ASIGNACION),
        "/=": (True, "/=", 2, Categoria.OPERADOR_ASIGNACION),
        "%=": (True, "%=", 2, Categoria.OPERADOR_ASIGNACION),
        "**=": (True, "**=", 3, Categoria.OPERADOR_ASIGNACION),
        "&&=": (True, "&&=", 3, Categoria.OPERADOR_ASIGNACION),
        "||=": (True, "||=", 3, Categoria.OPERADOR_ASIGNACION),
        "??=": (True, "??=", 3, Categoria.OPERADOR_ASIGNACION),
        
        # Operadores de incremento/decremento
        "++": (True, "++", 2, Categoria.OPERADOR_INCREMENTO),
        "--": (True, "--", 2, Categoria.OPERADOR_DECREMENTO),
        
        # Operadores de acceso
        ".": (True, ".", 1, Categoria.OPERADOR_ACCESO),
        "?.": (True, "?.", 2, Categoria.OPERADOR_ACCESO),
        "?.[": (True, "?.[", 3, Categoria.OPERADOR_ACCESO),
        "?.[]": (True, "?.[]", 4, Categoria.OPERADOR_ACCESO),
        
        # Operadores de TypeScript
        "?": (True, "?", 1, Categoria.OPERADOR_TYPESCRIPT),
        "??": (True, "??", 2, Categoria.OPERADOR_TYPESCRIPT),
        "|": (True, "|", 1, Categoria.OPERADOR_TYPESCRIPT),
        "&": (True, "&", 1, Categoria.OPERADOR_TYPESCRIPT),
        "<": (True, "<", 1, Categoria.OPERADOR_TYPESCRIPT),
        ">": (True, ">", 1, Categoria.OPERADOR_TYPESCRIPT),
        "${": (True, "${", 2, Categoria.OPERADOR_TYPESCRIPT),
        "}": (True, "}", 1, Categoria.OPERADOR_TYPESCRIPT),
        
        # Símbolos
        "(": (True, "(", 1, Categoria.PARENTESIS_IZQ),
        ")": (True, ")", 1, Categoria.PARENTESIS_DER),
        "{": (True, "{", 1, Categoria.LLAVE_IZQ),
        "}": (True, "}", 1, Categoria.LLAVE_DER),
        "[": (True, "[", 1, Categoria.CORCHETE_IZQ),
        "]": (True, "]", 1, Categoria.CORCHETE_DER),
        ";": (True, ";", 1, Categoria.PUNTO_Y_COMA),
        ",": (True, ",", 1, Categoria.COMA),
        ".": (True, ".", 1, Categoria.PUNTO),
        
        # Casos de error
        "": (False, "", 0, None),  # Vacío
        "a": (False, "", 0, None),  # No es un símbolo
        "abc": (False, "", 0, None),  # No es un símbolo
    }
    
    for prueba, esperado in pruebas.items():
        valido, lexema, consumidos, categoria = afd.analizar(prueba, 0)
        resultado = (valido, lexema, consumidos, categoria)
        print(f"Entrada: '{prueba}' -> Resultado: {resultado}, Esperado: {esperado} -> Correcto: {resultado == esperado}")
    
    print("--- Prueba específica para 'a+b' en pos 1 ---")
    texto_especifico = "a+b"
    valido, lexema, consumidos, categoria = afd.analizar(texto_especifico, 1) # Analizar "+"
    resultado_esp = (valido, lexema, consumidos, categoria)
    # Esperado: (True, "+", 1, Categoria.OPERADOR_ARITMETICO)
    esperado_esp = (True, "+", 1, Categoria.OPERADOR_ARITMETICO)
    print(f"Entrada: '{texto_especifico}' (desde pos 1) -> Resultado: {resultado_esp}, Esperado: {esperado_esp} -> Correcto: {resultado_esp == esperado_esp}") 