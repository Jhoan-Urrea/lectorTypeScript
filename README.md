# Analizador Léxico para JavaScript con Interfaz Gráfica Tkinter

Este proyecto implementa un analizador léxico para un subconjunto de JavaScript utilizando Autómatas Finitos Deterministas (AFD) y una interfaz gráfica desarrollada con Tkinter para facilitar la interacción.

## Características Principales

-   **Análisis Léxico Detallado**: Identifica y clasifica tokens como palabras reservadas, identificadores, números (naturales y reales), cadenas (con comillas simples, dobles y acentos graves), comentarios (de línea y bloque), operadores y símbolos.
-   **Interfaz Gráfica Interactiva**:
    -   Editor de texto para ingresar código JavaScript.
    -   Visualización en tiempo real de tokens identificados en una tabla (lexema, categoría, fila, columna).
    -   Coloreado de tokens en la tabla según su categoría para mejor legibilidad.
    -   Panel dedicado para mostrar errores léxicos encontrados.
    -   Botones para analizar el código y limpiar los campos.
-   **Manejo de Errores**: Reporta caracteres no reconocidos indicando su posición.
-   **Principio de Máxima Coincidencia**: El lexer prioriza el token más largo posible.
-   **Reglas Específicas**:
    -   Los identificadores se truncan a un máximo de 10 caracteres.

## Estructura del Proyecto

```
TLF_proyecto/
├── main.py                     # Punto de entrada para la aplicación (lanza la GUI)
├── gui/
│   └── interfaz.py             # Implementación de la interfaz gráfica con Tkinter
├── analizadores/
│   ├── identificador.py        # AFD para Identificadores (con truncamiento a 10 chars)
│   ├── numero_natural.py       # AFD para Números Naturales
│   ├── numero_real.py          # AFD para Números Reales (incluye notación científica básica)
│   ├── palabra_reservada.py    # AFD para Palabras Reservadas de JavaScript
│   ├── cadena.py               # AFD para Cadenas de texto ( "", \'\', `` ) con secuencias de escape
│   ├── comentario_linea.py     # AFD para Comentarios de Línea (//...)
│   ├── comentario_bloque.py    # AFD para Comentarios de Bloque (/*...*/)
│   └── simbolo.py              # AFD para Operadores y Símbolos (paréntesis, llaves, etc.)
├── lexer.py                    # Orquestador de los AFDs, realiza el análisis léxico completo
├── tokens.py                   # Definición de categorías de tokens (enum Categoria) y clase Token
├── tests/                      # Directorio para pruebas unitarias
│   ├── test_identificador.py
│   ├── test_numero_natural.py
│   ├── test_numero_real.py
│   ├── test_palabra_reservada.py
│   ├── test_cadena.py
│   ├── test_comentario_linea.py
│   ├── test_comentario_bloque.py
│   ├── test_simbolo.py
│   └── test_lexer.py           # Pruebas de integración para AnalizadorLexico
├── docs/                       # Documentación formal de los autómatas
│   └── automatas/              # Documentación de cada autómata con su expresión regular y diagrama
├── README.md                   # Este archivo
└── requirements.txt            # (Opcional, si se añaden dependencias externas)
```

## Documentación

Este proyecto incluye documentación detallada:

- [Documentación General](docs/README.md): Guía de uso, screenshots y descripción funcional
- [Documentación de Autómatas](docs/automatas/README.md): Expresiones regulares y diagramas de estados
- [Requisitos Cumplidos](docs/requisitos_cumplidos.md): Detalle de cómo se cumple cada requisito

## Requisitos

-   Python 3.6 o superior
-   Tkinter (generalmente incluido en las instalaciones estándar de Python)

Si Tkinter no está disponible en tu sistema (común en algunas instalaciones mínimas de Linux), puedes instalarlo. Por ejemplo, en sistemas basados en Debian/Ubuntu:

```bash
sudo apt-get update
sudo apt-get install python3-tk
```

## Ejecución

Para ejecutar la aplicación y abrir la interfaz gráfica:

```bash
python3 main.py
```
O si estás en la raíz del proyecto y `main.py` es ejecutable:
```bash
./main.py
```

## Analizadores Implementados

Todos los analizadores listados en la estructura del proyecto han sido implementados y probados:

-   **`IdentificadorAFD`**: Reconoce identificadores (letras, números, `_`, `$`), truncados a 10 caracteres.
-   **`NumeroNaturalAFD`**: Reconoce secuencias de dígitos.
-   **`NumeroRealAFD`**: Reconoce números con parte decimal y opcionalmente notación científica (ej: `123`, `123.45`, `1.2e3`, `0.5E-2`).
-   **`PalabraReservadaAFD`**: Reconoce palabras clave de JavaScript de una lista predefinida, asegurando que no sean prefijos de identificadores más largos.
-   **`CadenaAFD`**: Reconoce cadenas delimitadas por comillas dobles (`"`), simples (`\'\'\'`), o acentos graves (`` ` ``), incluyendo el manejo de secuencias de escape como `\\\"`, `\\\'`, `\\\``, `\\\\`, `\\n`, `\\t`.
-   **`ComentarioLineaAFD`**: Reconoce comentarios de una sola línea que comienzan con `//`.
-   **`ComentarioBloqueAFD`**: Reconoce comentarios de bloque encerrados entre `/*` y `*/`. (Nota: Actualmente no soporta bloques anidados de forma explícita, pero consumirá hasta el primer `*/`.)
-   **`SimboloAFD`**: Reconoce una amplia gama de operadores (aritméticos, lógicos, de comparación, asignación, acceso, etc.) y delimitadores (paréntesis, llaves, corchetes, punto y coma, coma, dos puntos, operadores con `?`).

## Pruebas Unitarias

El proyecto incluye un conjunto de pruebas unitarias en el directorio `tests/` para validar el comportamiento de cada AFD individual y la integración del `AnalizadorLexico`. Estas pruebas cubren diversos casos de éxito y error.

## Contribuciones

Las contribuciones son bienvenidas. Si deseas añadir nuevas funcionalidades o mejorar las existentes:

1.  Crea una nueva rama para tus cambios.
2.  Realiza tus modificaciones.
3.  Asegúrate de añadir o actualizar las pruebas unitarias correspondientes.
4.  Verifica que todas las pruebas pasen.
5.  Envía un Pull Request.

## Licencia

Este proyecto está bajo la licencia MIT. 
