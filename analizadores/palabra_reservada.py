import sys
import os

# Añadir la raíz del proyecto al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tokens import PALABRAS_RESERVADAS

class PalabraReservadaAFD:
    def __init__(self):
        self.palabras_reservadas = PALABRAS_RESERVADAS
        
    def analizar(self, texto, pos_inicial):
        """
        Verifica si a partir de la posición inicial hay una palabra reservada.
        Un lexema es una palabra reservada si es exactamente una de las PALABRAS_RESERVADAS
        y no está inmediatamente seguido por un carácter que podría formar parte de un 
        identificador más largo (letra, número, _, $).
        
        Args:
            texto: Cadena de texto a analizar
            pos_inicial: Posición desde donde comenzar el análisis
            
        Returns:
            Tupla de (es_valido, lexema, caracteres_consumidos)
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
                return False, '', 0
            else:
                # Es una palabra reservada y no está seguida por caracteres de identificador.
                # O es una palabra reservada al final del texto.
                return True, lexema_formado, len(lexema_formado)
        else:
            # El lexema formado no es una palabra reservada en absoluto.
            return False, '', 0

if __name__ == "__main__":
    # Pruebas
    afd = PalabraReservadaAFD()
    
    print("--- Pruebas del main de PalabraReservadaAFD ---")
    pruebas = {
        "if": (True, "if", 2),
        "for": (True, "for", 3),
        "while": (True, "while", 5),
        "ifx": (False, "", 0),          # No es palabra reservada (es identificador)
        "variable": (False, "", 0),     # No es palabra reservada (var es prefijo pero no es PR standalone)
        "function": (True, "function", 8),
        "functionX": (False, "", 0),    # No es palabra reservada (es identificador)
        "do": (True, "do", 2),
        "double": (False, "", 0),       # Asumiendo "double" NO es reservada.
        "class": (True, "class", 5),
        "123": (False, "", 0),          # No es palabra reservada
        "": (False, "", 0),             # Vacío
        "if(cond)": (True, "if", 2),    # "if" seguido de no-identificador
        "var x": (True, "var", 3)       # "var" seguido de espacio
    }

    for prueba, esperado in pruebas.items():
        valido, lexema, consumidos = afd.analizar(prueba, 0)
        resultado = (valido, lexema, consumidos)
        print(f"Entrada: '{prueba}' -> Resultado: {resultado}, Esperado: {esperado} -> Correcto: {resultado == esperado}")
    
    print("--- Prueba específica para '123if456' en pos 3 ---")
    texto_especifico = "123if456"
    valido, lexema, consumidos = afd.analizar(texto_especifico, 3) # Analizar "if456"
    resultado_esp = (valido, lexema, consumidos)
    # Esperado: (False, "", 0) porque "if" está seguido de "4"
    esperado_esp = (False, "", 0) 
    print(f"Entrada: '{texto_especifico}' (desde pos 3) -> Resultado: {resultado_esp}, Esperado: {esperado_esp} -> Correcto: {resultado_esp == esperado_esp}") 