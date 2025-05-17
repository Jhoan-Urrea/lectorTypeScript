class NumeroNaturalAFD:
    """
    Autómata Finito Determinista para reconocer números naturales en JavaScript.
    
    Los números naturales pueden ser:
    - El dígito 0 por sí solo
    - Una secuencia de dígitos que no comienza con 0
    """
    def __init__(self):
        """Inicializa el autómata."""
        pass

    def analizar(self, texto, pos_inicial):
        """
        Analiza si a partir de la posición inicial hay un número natural.
        
        Args:
            texto: Cadena de texto a analizar
            pos_inicial: Posición desde donde comenzar el análisis
            
        Returns:
            Tupla de (es_valido, lexema, caracteres_consumidos)
        """
        # Estados del autómata:
        # 0: Estado inicial
        # 1: Estado de aceptación (después de dígito distinto de 0)
        estado = 0
        lexema = ''  # Almacena el número que se va construyendo
        pos = pos_inicial  # Posición actual en el texto
        
        while pos < len(texto):
            c = texto[pos]  # Obtener carácter actual
            
            if estado == 0:  # Estado inicial
                if c.isdigit() and c != '0':
                    # Si es un dígito distinto de 0, pasamos al estado 1
                    estado = 1
                    lexema += c
                    pos += 1
                elif c == '0':
                    # El número 0 es un caso especial (solo el dígito)
                    lexema = c
                    return True, lexema, 1
                else:
                    break  # No es un número natural válido
            
            elif estado == 1:  # Ya tenemos un primer dígito válido (no 0)
                if c.isdigit():
                    # Continuar acumulando dígitos
                    lexema += c
                    pos += 1
                else:
                    break  # Fin del número
        
        # Verificar si el número es válido (estado de aceptación)
        if estado == 1:
            return True, lexema, pos - pos_inicial
        else:
            return False, '', 0

if __name__ == "__main__":
    # Código de prueba
    afd = NumeroNaturalAFD()
    
    pruebas = [
        "123",     # Número natural válido
        "0",       # Número natural válido (caso especial)
        "01",      # Solo reconoce el '0' (el 1 sería otro token)
        "abc",     # No es un número
        "123abc",  # Solo reconoce "123"
        ""         # Cadena vacía (no válida)
    ]
    
    for prueba in pruebas:
        valido, lexema, consumidos = afd.analizar(prueba, 0)
        print(f"Entrada: '{prueba}' -> Válido: {valido}, Lexema: '{lexema}', Caracteres consumidos: {consumidos}") 