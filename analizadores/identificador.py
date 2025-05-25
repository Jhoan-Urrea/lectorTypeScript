import sys
import os

# Añadir la raíz del proyecto al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tokens import Categoria

class IdentificadorAFD:
    """
    Autómata Finito Determinista para reconocer identificadores en TypeScript.
    
    Los identificadores en TypeScript deben:
    - Comenzar con una letra, guion bajo (_) o signo de dólar ($)
    - Luego pueden contener letras, números, guiones bajos o signos de dólar
    - No pueden ser palabras reservadas
    """
    def __init__(self):
        """
        Inicializa el autómata con la lista de palabras reservadas.
        """
        self.palabras_reservadas = {
            'if', 'else', 'while', 'for', 'do', 'switch', 'case', 'break', 'continue',
            'return', 'function', 'new', 'this', 'super', 'import', 'export', 'default',
            'string', 'number', 'boolean', 'any', 'unknown', 'never', 'void',
            'class', 'interface', 'type', 'enum', 'keyof', 'infer', 'as', 'readonly',
            'unique', 'override', 'extends', 'implements', 'namespace', 'module',
            'declare', 'abstract', 'async', 'await', 'static', 'private', 'protected',
            'public', 'get', 'set', 'in', 'instanceof', 'typeof', 'is', 'satisfies',
            'asserts', 'const', 'let', 'var', 'try', 'catch', 'finally', 'throw'
        }

    def analizar(self, texto, pos_inicial):
        """
        Verifica si a partir de la posición inicial hay un identificador válido.
        Un identificador en TypeScript puede comenzar con una letra, _ o $,
        y puede contener letras, números, _ o $.
        
        Args:
            texto: Cadena de texto a analizar
            pos_inicial: Posición desde donde comenzar el análisis
            
        Returns:
            Tupla de (es_valido, lexema, caracteres_consumidos, categoria)
        """
        # Ignorar espacios en blanco antes de buscar el identificador
        while pos_inicial < len(texto) and texto[pos_inicial].isspace():
            pos_inicial += 1
        if pos_inicial >= len(texto):
            return False, '', 0, None
            
        # Verificar el primer carácter
        primer_caracter = texto[pos_inicial]
        if not (primer_caracter.isalpha() or primer_caracter == '_' or primer_caracter == '$'):
            return False, '', 0, None
            
        # Formar el lexema
        lexema = primer_caracter
        pos_actual = pos_inicial + 1
        
        # Continuar mientras haya caracteres válidos
        while pos_actual < len(texto):
            caracter = texto[pos_actual]
            # Solo permitir letras, números, guiones bajos y signos de dólar
            if not (caracter.isalnum() or caracter == '_' or caracter == '$'):
                # Si encontramos un carácter inválido, rechazamos todo el identificador
                return False, '', 0, None
            lexema += caracter
            pos_actual += 1
        
        # Verificar si es una palabra reservada
        if lexema in self.palabras_reservadas:
            return False, '', 0, None
                
        return True, lexema, len(lexema), Categoria.IDENTIFICADOR

if __name__ == "__main__":
    # Pruebas
    afd = IdentificadorAFD()
    
    print("--- Pruebas del main de IdentificadorAFD ---")
    pruebas = {
        "variable": (True, "variable", 8, Categoria.IDENTIFICADOR),
        "_variable": (True, "_variable", 9, Categoria.IDENTIFICADOR),
        "$variable": (True, "$variable", 9, Categoria.IDENTIFICADOR),
        "variable123": (True, "variable123", 11, Categoria.IDENTIFICADOR),
        "variable_123": (True, "variable_123", 11, Categoria.IDENTIFICADOR),
        "variable$123": (True, "variable$123", 11, Categoria.IDENTIFICADOR),
        "123variable": (False, "", 0, None),  # No puede comenzar con número
        "@variable": (False, "", 0, None),    # No puede comenzar con @
        "": (False, "", 0, None),             # Vacío
        "if": (False, "", 0, None),           # Palabra reservada
        "class": (False, "", 0, None),        # Palabra reservada
        "interface": (False, "", 0, None),    # Palabra reservada
        "type": (False, "", 0, None),         # Palabra reservada
        "enum": (False, "", 0, None),         # Palabra reservada
        "keyof": (False, "", 0, None),        # Palabra reservada
        "infer": (False, "", 0, None),        # Palabra reservada
        "as": (False, "", 0, None),           # Palabra reservada
        "readonly": (False, "", 0, None),     # Palabra reservada
        "unique": (False, "", 0, None),       # Palabra reservada
        "override": (False, "", 0, None),     # Palabra reservada
        "extends": (False, "", 0, None),      # Palabra reservada
        "implements": (False, "", 0, None),   # Palabra reservada
        "namespace": (False, "", 0, None),    # Palabra reservada
        "module": (False, "", 0, None),       # Palabra reservada
        "declare": (False, "", 0, None),      # Palabra reservada
        "abstract": (False, "", 0, None),     # Palabra reservada
        "async": (False, "", 0, None),        # Palabra reservada
        "await": (False, "", 0, None),        # Palabra reservada
        "static": (False, "", 0, None),       # Palabra reservada
        "private": (False, "", 0, None),      # Palabra reservada
        "protected": (False, "", 0, None),    # Palabra reservada
        "public": (False, "", 0, None),       # Palabra reservada
        "get": (False, "", 0, None),          # Palabra reservada
        "set": (False, "", 0, None),          # Palabra reservada
        "in": (False, "", 0, None),           # Palabra reservada
        "instanceof": (False, "", 0, None),   # Palabra reservada
        "typeof": (False, "", 0, None),       # Palabra reservada
        "is": (False, "", 0, None),           # Palabra reservada
        "satisfies": (False, "", 0, None),    # Palabra reservada
        "asserts": (False, "", 0, None),      # Palabra reservada
        "const": (False, "", 0, None),        # Palabra reservada
        "let": (False, "", 0, None),          # Palabra reservada
        "var": (False, "", 0, None),          # Palabra reservada
        "try": (False, "", 0, None),          # Palabra reservada
        "catch": (False, "", 0, None),        # Palabra reservada
        "finally": (False, "", 0, None),      # Palabra reservada
        "throw": (False, "", 0, None),        # Palabra reservada
        "if": (False, "", 0, None),           # Palabra reservada
        "else": (False, "", 0, None),         # Palabra reservada
        "while": (False, "", 0, None),        # Palabra reservada
        "for": (False, "", 0, None),          # Palabra reservada
        "do": (False, "", 0, None),           # Palabra reservada
        "switch": (False, "", 0, None),       # Palabra reservada
        "case": (False, "", 0, None),         # Palabra reservada
        "break": (False, "", 0, None),        # Palabra reservada
        "continue": (False, "", 0, None),     # Palabra reservada
        "return": (False, "", 0, None),       # Palabra reservada
        "function": (False, "", 0, None),     # Palabra reservada
        "new": (False, "", 0, None),          # Palabra reservada
        "this": (False, "", 0, None),         # Palabra reservada
        "super": (False, "", 0, None),        # Palabra reservada
        "import": (False, "", 0, None),       # Palabra reservada
        "export": (False, "", 0, None),       # Palabra reservada
        "default": (False, "", 0, None),      # Palabra reservada
        "string": (False, "", 0, None),       # Palabra reservada
        "number": (False, "", 0, None),       # Palabra reservada
        "boolean": (False, "", 0, None),      # Palabra reservada
        "any": (False, "", 0, None),          # Palabra reservada
        "unknown": (False, "", 0, None),      # Palabra reservada
        "never": (False, "", 0, None),        # Palabra reservada
        "void": (False, "", 0, None),         # Palabra reservada
    }
    
    for prueba, esperado in pruebas.items():
        valido, lexema, consumidos, categoria = afd.analizar(prueba, 0)
        resultado = (valido, lexema, consumidos, categoria)
        print(f"Entrada: '{prueba}' -> Resultado: {resultado}, Esperado: {esperado} -> Correcto: {resultado == esperado}")
    
    print("--- Prueba específica para '123variable' en pos 3 ---")
    texto_especifico = "123variable"
    valido, lexema, consumidos, categoria = afd.analizar(texto_especifico, 3) # Analizar "variable"
    resultado_esp = (valido, lexema, consumidos, categoria)
    # Esperado: (True, "variable", 8, Categoria.IDENTIFICADOR)
    esperado_esp = (True, "variable", 8, Categoria.IDENTIFICADOR)
    print(f"Entrada: '{texto_especifico}' (desde pos 3) -> Resultado: {resultado_esp}, Esperado: {esperado_esp} -> Correcto: {resultado_esp == esperado_esp}") 