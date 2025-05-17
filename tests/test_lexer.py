import pytest
import sys
import os

# Añadir la raíz del proyecto al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lexer import AnalizadorLexico
from tokens import Token, Categoria

@pytest.fixture
def lexer():
    return AnalizadorLexico()

class TestAnalizadorLexico:
    def test_declaracion_variable_simple(self, lexer):
        codigo = "var x = 10;"
        tokens_esperados = [
            Token("var", Categoria.PALABRA_RESERVADA, 1, 1),
            Token("x", Categoria.IDENTIFICADOR, 1, 5),
            Token("=", Categoria.OPERADOR_ASIGNACION, 1, 7),
            Token("10", Categoria.NUMERO_NATURAL, 1, 9),
            Token(";", Categoria.TERMINAL, 1, 11)
        ]
        
        tokens_obtenidos, errores = lexer.analizar(codigo)
        
        assert not errores, f"Se encontraron errores inesperados: {errores}"
        assert len(tokens_obtenidos) == len(tokens_esperados), \
               f"Se esperaban {len(tokens_esperados)} tokens pero se obtuvieron {len(tokens_obtenidos)}"
        
        for i, token_esperado in enumerate(tokens_esperados):
            token_obtenido = tokens_obtenidos[i]
            assert token_obtenido.lexema == token_esperado.lexema, \
                   f"Token {i}: Lexema esperado '{token_esperado.lexema}', obtenido '{token_obtenido.lexema}'"
            assert token_obtenido.categoria == token_esperado.categoria, \
                   f"Token {i} ('{token_obtenido.lexema}'): Categoría esperada '{token_esperado.categoria}', obtenida '{token_obtenido.categoria}'"
            assert token_obtenido.fila == token_esperado.fila, \
                   f"Token {i} ('{token_obtenido.lexema}'): Fila esperada {token_esperado.fila}, obtenida {token_obtenido.fila}"
            assert token_obtenido.columna == token_esperado.columna, \
                   f"Token {i} ('{token_obtenido.lexema}'): Columna esperada {token_esperado.columna}, obtenida {token_obtenido.columna}"

    def test_funcion_compleja(self, lexer):
        codigo = """// Función de ejemplo para probar el lexer
function calcularTotal(precio, cantidad) {
    const IMPUESTO = 0.15; // Impuesto fijo del 15%
    let subtotal = precio * cantidad;
    /* Calcular impuesto y total */
    let impuestoCalculado = subtotal * IMPUESTO;
    let totalFinal = subtotal + impuestoCalculado;

    if (totalFinal > 100.0) {
        console.log(\"¡Compra grande!\");
    }
    return totalFinal;
}"""
        tokens_esperados = [
            Token("// Función de ejemplo para probar el lexer", Categoria.COMENTARIO_LINEA, 1, 1),
            Token("function", Categoria.PALABRA_RESERVADA, 2, 1),
            Token("calcularTo", Categoria.IDENTIFICADOR, 2, 10),
            Token("tal", Categoria.IDENTIFICADOR, 2, 20),
            Token("(", Categoria.PARENTESIS_APERTURA, 2, 23),
            Token("precio", Categoria.IDENTIFICADOR, 2, 24),
            Token(",", Categoria.SEPARADOR, 2, 30),
            Token("cantidad", Categoria.IDENTIFICADOR, 2, 32),
            Token(")", Categoria.PARENTESIS_CIERRE, 2, 40),
            Token("{", Categoria.LLAVE_APERTURA, 2, 42),
            Token("const", Categoria.PALABRA_RESERVADA, 3, 5),
            Token("IMPUESTO", Categoria.IDENTIFICADOR, 3, 11),
            Token("=", Categoria.OPERADOR_ASIGNACION, 3, 20),
            Token("0.15", Categoria.NUMERO_REAL, 3, 22),
            Token(";", Categoria.TERMINAL, 3, 26),
            Token("// Impuesto fijo del 15%", Categoria.COMENTARIO_LINEA, 3, 28),
            Token("let", Categoria.PALABRA_RESERVADA, 4, 5),
            Token("subtotal", Categoria.IDENTIFICADOR, 4, 9),
            Token("=", Categoria.OPERADOR_ASIGNACION, 4, 18),
            Token("precio", Categoria.IDENTIFICADOR, 4, 20),
            Token("*", Categoria.OPERADOR_ARITMETICO, 4, 27),
            Token("cantidad", Categoria.IDENTIFICADOR, 4, 29),
            Token(";", Categoria.TERMINAL, 4, 37),
            Token("/* Calcular impuesto y total */", Categoria.COMENTARIO_BLOQUE, 5, 5),
            Token("let", Categoria.PALABRA_RESERVADA, 6, 5),
            Token("impuestoCa", Categoria.IDENTIFICADOR, 6, 9),
            Token("lculado", Categoria.IDENTIFICADOR, 6, 19),
            Token("=", Categoria.OPERADOR_ASIGNACION, 6, 27),
            Token("subtotal", Categoria.IDENTIFICADOR, 6, 29),
            Token("*", Categoria.OPERADOR_ARITMETICO, 6, 38),
            Token("IMPUESTO", Categoria.IDENTIFICADOR, 6, 40),
            Token(";", Categoria.TERMINAL, 6, 48),
            Token("let", Categoria.PALABRA_RESERVADA, 7, 5),
            Token("totalFinal", Categoria.IDENTIFICADOR, 7, 9),
            Token("=", Categoria.OPERADOR_ASIGNACION, 7, 20),
            Token("subtotal", Categoria.IDENTIFICADOR, 7, 22),
            Token("+", Categoria.OPERADOR_ARITMETICO, 7, 31),
            Token("impuestoCa", Categoria.IDENTIFICADOR, 7, 33),
            Token("lculado", Categoria.IDENTIFICADOR, 7, 43),
            Token(";", Categoria.TERMINAL, 7, 50),
            Token("if", Categoria.PALABRA_RESERVADA, 9, 5),
            Token("(", Categoria.PARENTESIS_APERTURA, 9, 8),
            Token("totalFinal", Categoria.IDENTIFICADOR, 9, 9),
            Token(">", Categoria.OPERADOR_COMPARACION, 9, 20),
            Token("100.0", Categoria.NUMERO_REAL, 9, 22),
            Token(")", Categoria.PARENTESIS_CIERRE, 9, 27),
            Token("{", Categoria.LLAVE_APERTURA, 9, 29),
            Token("console", Categoria.IDENTIFICADOR, 10, 9),
            Token(".", Categoria.OPERADOR_ACCESO, 10, 16),
            Token("log", Categoria.IDENTIFICADOR, 10, 17),
            Token("(", Categoria.PARENTESIS_APERTURA, 10, 20),
            Token("\"¡Compra grande!\"", Categoria.CADENA, 10, 21),
            Token(")", Categoria.PARENTESIS_CIERRE, 10, 38),
            Token(";", Categoria.TERMINAL, 10, 39),
            Token("}", Categoria.LLAVE_CIERRE, 11, 5),
            Token("return", Categoria.PALABRA_RESERVADA, 12, 5),
            Token("totalFinal", Categoria.IDENTIFICADOR, 12, 12),
            Token(";", Categoria.TERMINAL, 12, 22),
            Token("}", Categoria.LLAVE_CIERRE, 13, 1)
        ]

        tokens_obtenidos, errores = lexer.analizar(codigo)
        
        assert not errores, f"Se encontraron errores inesperados: {errores}"
        
        # Imprimir tokens para depuración si falla la longitud
        if len(tokens_obtenidos) != len(tokens_esperados):
            print("Tokens obtenidos:")
            for t_o in tokens_obtenidos:
                print(f"  Token('{t_o.lexema}', Categoria.{t_o.categoria.split('.')[-1]}, {t_o.fila}, {t_o.columna})")
            print("\\nTokens esperados:")
            for t_e in tokens_esperados:
                print(f"  Token('{t_e.lexema}', Categoria.{t_e.categoria.split('.')[-1]}, {t_e.fila}, {t_e.columna})")

        assert len(tokens_obtenidos) == len(tokens_esperados), \
               f"Se esperaban {len(tokens_esperados)} tokens pero se obtuvieron {len(tokens_obtenidos)}"
        
        for i, token_esperado in enumerate(tokens_esperados):
            token_obtenido = tokens_obtenidos[i]
            assert token_obtenido.lexema == token_esperado.lexema, \
                   f"Token {i} (Fila {token_esperado.fila}, Col {token_esperado.columna}): Lexema esperado '{token_esperado.lexema}', obtenido '{token_obtenido.lexema}'"
            assert token_obtenido.categoria == token_esperado.categoria, \
                   f"Token {i} ('{token_obtenido.lexema}' F{token_obtenido.fila}C{token_obtenido.columna}): Categoría esperada '{token_esperado.categoria}', obtenida '{token_obtenido.categoria}'"
            assert token_obtenido.fila == token_esperado.fila, \
                   f"Token {i} ('{token_obtenido.lexema}'): Fila esperada {token_esperado.fila}, obtenida {token_obtenido.fila}"
            assert token_obtenido.columna == token_esperado.columna, \
                   f"Token {i} ('{token_obtenido.lexema}'): Columna esperada {token_esperado.columna}, obtenida {token_obtenido.columna}"

    # Aquí podemos añadir más pruebas para el AnalizadorLexico 