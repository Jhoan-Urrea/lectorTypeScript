import sys
import os

# Añadir la raíz del proyecto al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tokens import PALABRAS_RESERVADAS, Categoria

class PalabraReservadaAFD:
    def __init__(self):
        self.palabras_reservadas = PALABRAS_RESERVADAS
        
    def analizar(self, texto, pos_inicial):
        """
        Verifica si a partir de la posición inicial hay una palabra reservada.
        Si es un tipo primitivo, devuelve la categoría TIPO_PRIMITIVO.
        Un lexema es una palabra reservada si es exactamente una de las PALABRAS_RESERVADAS
        y no está inmediatamente seguido por un carácter que podría formar parte de un 
        identificador más largo (letra, número, _, $).
        
        Args:
            texto: Cadena de texto a analizar
            pos_inicial: Posición desde donde comenzar el análisis
            
        Returns:
            Tupla de (es_valido, lexema, caracteres_consumidos, categoria)
        """
        lexema_formado = ''
        pos_actual = pos_inicial
        
        # 1. Formar el lexema potencial más largo con caracteres válidos para identificadores
        while pos_actual < len(texto) and \
              (texto[pos_actual].isalnum() or texto[pos_actual] == '_' or texto[pos_actual] == '$'):
            lexema_formado += texto[pos_actual]
            pos_actual += 1
            
        # 2. Verificar si este lexema_formado es una palabra reservada
        if lexema_formado in self.palabras_reservadas:
            # 3. Verificar el carácter inmediatamente siguiente en el texto original
            #    (si es que hay uno) para asegurar que no es parte de un identificador más largo.
            if pos_actual < len(texto) and \
               (texto[pos_actual].isalnum() or texto[pos_actual] == '_' or texto[pos_actual] == '$'):
                # Es parte de un identificador más largo (ej: "ifx", "variable")
                # Por lo tanto, este AFD no debe reconocerlo como palabra reservada.
                return False, '', 0, None
            else:
                # Es una palabra reservada
                return True, lexema_formado, len(lexema_formado), self.palabras_reservadas[lexema_formado]
        else:
            # El lexema formado no es una palabra reservada en absoluto.
            return False, '', 0, None

if __name__ == "__main__":
    # Pruebas
    afd = PalabraReservadaAFD()
    
    print("--- Pruebas del main de PalabraReservadaAFD ---")
    pruebas = {
        "if": (True, "if", 2, Categoria.PALABRA_RESERVADA),
        "for": (True, "for", 3, Categoria.PALABRA_RESERVADA),
        "while": (True, "while", 5, Categoria.PALABRA_RESERVADA),
        "ifx": (False, "", 0, None),          # No es palabra reservada (es identificador)
        "variable": (False, "", 0, None),     # No es palabra reservada (var es prefijo pero no es PR standalone)
        "function": (True, "function", 8, Categoria.PALABRA_RESERVADA),
        "functionX": (False, "", 0, None),    # No es palabra reservada (es identificador)
        "do": (True, "do", 2, Categoria.PALABRA_RESERVADA),
        "double": (False, "", 0, None),       # Asumiendo "double" NO es reservada.
        "class": (True, "class", 5, Categoria.PALABRA_RESERVADA),
        "123": (False, "", 0, None),          # No es palabra reservada
        "": (False, "", 0, None),             # Vacío
        "if(cond)": (True, "if", 2, Categoria.PALABRA_RESERVADA),    # "if" seguido de no-identificador
        "var x": (True, "var", 3, Categoria.PALABRA_RESERVADA),      # "var" seguido de espacio
        
        # Pruebas de tipos de TypeScript
        "string": (True, "string", 6, Categoria.TIPO_PRIMITIVO),
        "number": (True, "number", 6, Categoria.TIPO_PRIMITIVO),
        "boolean": (True, "boolean", 7, Categoria.TIPO_PRIMITIVO),
        "any": (True, "any", 3, Categoria.TIPO_PRIMITIVO),
        "unknown": (True, "unknown", 7, Categoria.TIPO_PRIMITIVO),
        "never": (True, "never", 5, Categoria.TIPO_PRIMITIVO),
        "void": (True, "void", 4, Categoria.TIPO_PRIMITIVO),
        
        # Pruebas de tipos especiales
        "interface": (True, "interface", 9, Categoria.TIPO_INTERFACE),
        "type": (True, "type", 4, Categoria.TIPO_TYPE),
        "enum": (True, "enum", 4, Categoria.TIPO_ENUM),
        "keyof": (True, "keyof", 5, Categoria.TIPO_KEYOF),
        "infer": (True, "infer", 5, Categoria.TIPO_INFER)
    }
    
    for prueba, esperado in pruebas.items():
        valido, lexema, consumidos, categoria = afd.analizar(prueba, 0)
        resultado = (valido, lexema, consumidos, categoria)
        print(f"Entrada: '{prueba}' -> Resultado: {resultado}, Esperado: {esperado} -> Correcto: {resultado == esperado}")
    
    print("--- Prueba específica para '123if456' en pos 3 ---")
    texto_especifico = "123if456"
    valido, lexema, consumidos, categoria = afd.analizar(texto_especifico, 3) # Analizar "if456"
    resultado_esp = (valido, lexema, consumidos, categoria)
    # Esperado: (False, "", 0, None) porque "if" está seguido de "4"
    esperado_esp = (False, "", 0, None) 
    print(f"Entrada: '{texto_especifico}' (desde pos 3) -> Resultado: {resultado_esp}, Esperado: {esperado_esp} -> Correcto: {resultado_esp == esperado_esp}") 