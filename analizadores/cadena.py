import sys
import os

# Añadir la raíz del proyecto al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tokens import Categoria

class CadenaAFD:
    def __init__(self):
        pass
        
    def analizar(self, texto, pos_inicial):
        """
        Verifica si a partir de la posición inicial hay una cadena válida.
        Una cadena en TypeScript puede ser:
        - Comillas simples: 'texto'
        - Comillas dobles: "texto"
        - Template literals: `texto`
        
        Args:
            texto: Cadena de texto a analizar
            pos_inicial: Posición desde donde comenzar el análisis
            
        Returns:
            Tupla de (es_valido, lexema, caracteres_consumidos, categoria)
        """
        if pos_inicial >= len(texto):
            return False, '', 0, None
            
        # Verificar el tipo de comilla
        comilla = texto[pos_inicial]
        if comilla not in ['"', "'", '`']:
            return False, '', 0, None
            
        # Formar el lexema
        lexema = comilla
        pos_actual = pos_inicial + 1
        escape = False
        
        # Continuar mientras no encontremos la comilla de cierre
        while pos_actual < len(texto):
            caracter = texto[pos_actual]
            
            # Si encontramos la comilla de cierre y no estamos escapando
            if caracter == comilla and not escape:
                lexema += caracter
                pos_actual += 1
                return True, lexema, len(lexema), Categoria.CADENA
                
            # Si encontramos un salto de línea y no estamos escapando
            if caracter == '\n' and not escape and comilla != '`':
                return False, '', 0, None
                
            # Si encontramos un escape
            if caracter == '\\' and not escape:
                escape = True
                lexema += caracter
                pos_actual += 1
                continue
                
            # Si estamos escapando, permitir cualquier carácter
            if escape:
                escape = False
                lexema += caracter
                pos_actual += 1
                continue
                
            # Carácter normal
            lexema += caracter
            pos_actual += 1
            
        # Si llegamos aquí, no encontramos la comilla de cierre
        return False, '', 0, None

if __name__ == "__main__":
    # Pruebas
    afd = CadenaAFD()
    
    print("--- Pruebas del main de CadenaAFD ---")
    pruebas = {
        # Cadenas con comillas dobles
        '"Hola"': (True, '"Hola"', 6, Categoria.CADENA),
        '"Hola mundo"': (True, '"Hola mundo"', 12, Categoria.CADENA),
        '"Hola\\nMundo"': (True, '"Hola\\nMundo"', 13, Categoria.CADENA),
        '"Hola\\"Mundo"': (True, '"Hola\\"Mundo"', 13, Categoria.CADENA),
        '"Hola\\\'Mundo"': (True, '"Hola\\\'Mundo"', 13, Categoria.CADENA),
        '"Hola\\`Mundo"': (True, '"Hola\\`Mundo"', 13, Categoria.CADENA),
        '"Hola\\tMundo"': (True, '"Hola\\tMundo"', 13, Categoria.CADENA),
        '"Hola\\rMundo"': (True, '"Hola\\rMundo"', 13, Categoria.CADENA),
        '"Hola\\bMundo"': (True, '"Hola\\bMundo"', 13, Categoria.CADENA),
        '"Hola\\fMundo"': (True, '"Hola\\fMundo"', 13, Categoria.CADENA),
        '"Hola\\vMundo"': (True, '"Hola\\vMundo"', 13, Categoria.CADENA),
        '"Hola\\0Mundo"': (True, '"Hola\\0Mundo"', 13, Categoria.CADENA),
        '"Hola\\x41Mundo"': (True, '"Hola\\x41Mundo"', 14, Categoria.CADENA),
        '"Hola\\u0041Mundo"': (True, '"Hola\\u0041Mundo"', 16, Categoria.CADENA),
        '"Hola\\u{41}Mundo"': (True, '"Hola\\u{41}Mundo"', 15, Categoria.CADENA),
        
        # Cadenas con comillas simples
        "'Hola'": (True, "'Hola'", 6, Categoria.CADENA),
        "'Hola mundo'": (True, "'Hola mundo'", 12, Categoria.CADENA),
        "'Hola\\nMundo'": (True, "'Hola\\nMundo'", 13, Categoria.CADENA),
        "'Hola\\\"Mundo'": (True, "'Hola\\\"Mundo'", 13, Categoria.CADENA),
        "'Hola\\'Mundo'": (True, "'Hola\\'Mundo'", 13, Categoria.CADENA),
        "'Hola\\`Mundo'": (True, "'Hola\\`Mundo'", 13, Categoria.CADENA),
        
        # Template literals
        "`Hola`": (True, "`Hola`", 6, Categoria.CADENA),
        "`Hola mundo`": (True, "`Hola mundo`", 12, Categoria.CADENA),
        "`Hola\\nMundo`": (True, "`Hola\\nMundo`", 13, Categoria.CADENA),
        "`Hola\\\"Mundo`": (True, "`Hola\\\"Mundo`", 13, Categoria.CADENA),
        "`Hola\\'Mundo`": (True, "`Hola\\'Mundo`", 13, Categoria.CADENA),
        "`Hola\\`Mundo`": (True, "`Hola\\`Mundo`", 13, Categoria.CADENA),
        "`Hola ${nombre}`": (True, "`Hola ${nombre}`", 15, Categoria.CADENA),
        "`Hola ${nombre + ' ' + apellido}`": (True, "`Hola ${nombre + ' ' + apellido}`", 31, Categoria.CADENA),
        
        # Casos de error
        "": (False, "", 0, None),  # Vacío
        "Hola": (False, "", 0, None),  # No comienza con comilla
        '"Hola': (False, "", 0, None),  # No tiene comilla de cierre
        "'Hola": (False, "", 0, None),  # No tiene comilla de cierre
        "`Hola": (False, "", 0, None),  # No tiene comilla de cierre
        '"Hola\nMundo"': (False, "", 0, None),  # Salto de línea no escapado
        "'Hola\nMundo'": (False, "", 0, None),  # Salto de línea no escapado
        '"Hola\\"': (False, "", 0, None),  # Escape al final
        "'Hola\\'": (False, "", 0, None),  # Escape al final
        "`Hola\\`": (False, "", 0, None),  # Escape al final
    }
    
    for prueba, esperado in pruebas.items():
        valido, lexema, consumidos, categoria = afd.analizar(prueba, 0)
        resultado = (valido, lexema, consumidos, categoria)
        print(f"Entrada: '{prueba}' -> Resultado: {resultado}, Esperado: {esperado} -> Correcto: {resultado == esperado}")
    
    print("--- Prueba específica para 'Hola\"Mundo' en pos 4 ---")
    texto_especifico = 'Hola"Mundo'
    valido, lexema, consumidos, categoria = afd.analizar(texto_especifico, 4) # Analizar "Mundo"
    resultado_esp = (valido, lexema, consumidos, categoria)
    # Esperado: (True, '"Mundo"', 6, Categoria.CADENA)
    esperado_esp = (True, '"Mundo"', 6, Categoria.CADENA)
    print(f"Entrada: '{texto_especifico}' (desde pos 4) -> Resultado: {resultado_esp}, Esperado: {esperado_esp} -> Correcto: {resultado_esp == esperado_esp}") 