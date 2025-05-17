class NumeroRealAFD:
    def __init__(self):
        pass

    def analizar(self, texto, pos_inicial):
        """
        Analiza si a partir de la posición inicial hay un número real.
        Un número real DEBE tener punto decimal o notación científica.
        Los números enteros sin punto decimal ni notación científica son detectados por el analizador de números naturales.
        
        Args:
            texto: Cadena de texto a analizar
            pos_inicial: Posición desde donde comenzar el análisis
            
        Returns:
            Tupla de (es_valido, lexema, caracteres_consumidos)
        """
        # Estados del autómata:
        # 0: Inicial
        # 1: Entero
        # 2: Punto después de dígito
        # 3: Dígitos después del punto
        # 4: Punto inicial (sin dígitos previos)
        # 5: Dígitos después del punto inicial
        # 6: 'e' o 'E' encontrada
        # 7: Signo después de 'e'
        # 8: Dígitos después de 'e' o después del signo
        
        estado = 0
        lexema = ''
        pos = pos_inicial
        
        # Flags para verificar que sea realmente un número real
        tiene_punto_decimal = False
        tiene_notacion_cientifica = False
        
        # Variables para guardar el último estado de aceptación
        ultimo_estado_aceptacion = None
        lexema_aceptado = ''
        pos_aceptado = pos_inicial
        
        while pos < len(texto):
            c = texto[pos]
            
            if estado == 0:  # Estado inicial
                if c.isdigit():
                    estado = 1
                    lexema += c
                    pos += 1
                elif c == '.':
                    estado = 4
                    lexema += c
                    pos += 1
                    tiene_punto_decimal = True
                else:
                    break
                    
            elif estado == 1:  # Entero (dígitos)
                if c.isdigit():
                    lexema += c
                    pos += 1
                elif c == '.':
                    estado = 2
                    lexema += c
                    pos += 1
                    tiene_punto_decimal = True
                elif c in 'eE':
                    estado = 6
                    lexema += c
                    pos += 1
                    tiene_notacion_cientifica = True
                else:
                    break
                    
            elif estado == 2:  # Punto después de dígitos
                if c.isdigit():
                    estado = 3
                    lexema += c
                    pos += 1
                elif c in 'eE':
                    estado = 6
                    lexema += c
                    pos += 1
                    tiene_notacion_cientifica = True
                else:
                    break
                    
            elif estado == 3:  # Dígitos después del punto
                if c.isdigit():
                    lexema += c
                    pos += 1
                elif c in 'eE':
                    estado = 6
                    lexema += c
                    pos += 1
                    tiene_notacion_cientifica = True
                else:
                    break
                    
            elif estado == 4:  # Punto inicial (sin dígitos previos)
                if c.isdigit():
                    estado = 5
                    lexema += c
                    pos += 1
                else:
                    break
                    
            elif estado == 5:  # Dígitos después del punto inicial
                if c.isdigit():
                    lexema += c
                    pos += 1
                elif c in 'eE':
                    estado = 6
                    lexema += c
                    pos += 1
                    tiene_notacion_cientifica = True
                else:
                    break
                    
            elif estado == 6:  # 'e' o 'E' encontrada
                if c.isdigit():
                    estado = 8
                    lexema += c
                    pos += 1
                elif c in '+-':
                    estado = 7
                    lexema += c
                    pos += 1
                else:
                    break
                    
            elif estado == 7:  # Signo después de 'e'
                if c.isdigit():
                    estado = 8
                    lexema += c
                    pos += 1
                else:
                    break
                    
            elif estado == 8:  # Dígitos después de 'e' o después del signo
                if c.isdigit():
                    lexema += c
                    pos += 1
                else:
                    break
            
            # Guardar el último estado de aceptación
            estados_aceptacion = [2, 3, 5, 8]
            if estado == 1 and tiene_notacion_cientifica:
                estados_aceptacion.append(1)
            if estado in estados_aceptacion and (tiene_punto_decimal or tiene_notacion_cientifica):
                ultimo_estado_aceptacion = estado
                lexema_aceptado = lexema
                pos_aceptado = pos
        
        # Al terminar, retornar el último lexema aceptado si existe
        if ultimo_estado_aceptacion is not None:
            return True, lexema_aceptado, pos_aceptado - pos_inicial
        else:
            return False, '', 0

if __name__ == "__main__":
    # Pruebas
    afd = NumeroRealAFD()
    
    pruebas = [
        "123.45",       # Real con punto decimal
        "0.5",          # Real con punto decimal
        ".5",           # Real con punto decimal
        "123e10",       # Real con notación científica
        "123.45e-10",   # Real con punto decimal y notación científica
        "123.",         # Real con punto decimal
        "123",          # Natural (no debería ser reconocido como real)
        "123e",         # Incompleto
        "123e+",        # Incompleto
        "e10",          # Incompleto
        "abc",          # No es un número
        "123.45.67",    # Inválido
        ""              # Vacío
    ]
    
    for prueba in pruebas:
        valido, lexema, consumidos = afd.analizar(prueba, 0)
        print(f"Entrada: '{prueba}' -> Válido: {valido}, Lexema: '{lexema}', Caracteres consumidos: {consumidos}") 