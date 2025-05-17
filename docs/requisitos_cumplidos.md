# Cumplimiento de Requisitos del Proyecto

Este documento detalla cómo el proyecto cumple con cada uno de los requisitos especificados.

## 1. Objetivos generales

✅ **Elaborar los autómatas finitos deterministas que acepten los tokens de un lenguaje de programación**
   - Se han implementado 8 autómatas finitos deterministas para reconocer todos los tokens requeridos
   - Cada autómata está documentado con su expresión regular y diagrama de estados

✅ **Implementar el software para el analizador léxico con interfaz gráfica**
   - Se ha desarrollado una interfaz gráfica utilizando Tkinter
   - La implementación está en Python, uno de los lenguajes permitidos

## 2. Tokens del lenguaje de programación

El analizador léxico reconoce todos los tokens requeridos:

✅ **Números Naturales**: Implementado en `analizadores/numero_natural.py`

✅ **Números Reales**: Implementado en `analizadores/numero_real.py`

✅ **Identificadores**: Implementado en `analizadores/identificador.py` (limitados a 10 caracteres)

✅ **Palabras Reservadas**: Implementado en `analizadores/palabra_reservada.py` (más de 6 palabras)

✅ **Operadores Aritméticos**: Implementado en `analizadores/simbolo.py` (+, -, *, /, %)

✅ **Operadores de Comparación**: Implementado en `analizadores/simbolo.py` (==, ===, !=, !==, <, >, <=, >=)

✅ **Operadores Lógicos**: Implementado en `analizadores/simbolo.py` (&&, ||, !)

✅ **Operadores de Asignación**: Implementado en `analizadores/simbolo.py` (=, +=, -=, *=, /=, %=)

✅ **Operadores de Incremento/Decremento**: Implementado en `analizadores/simbolo.py` (++, --)

✅ **Paréntesis**: Implementado en `analizadores/simbolo.py` ((, ))

✅ **Llaves**: Implementado en `analizadores/simbolo.py` ({, })

✅ **Terminal**: Implementado en `analizadores/simbolo.py` (;)

✅ **Separador**: Implementado en `analizadores/simbolo.py` (,)

✅ **Cadenas de Caracteres**: Implementado en `analizadores/cadena.py` (con manejo de secuencias de escape)

✅ **Comentarios de Línea**: Implementado en `analizadores/comentario_linea.py` (//)

✅ **Comentarios de Bloque**: Implementado en `analizadores/comentario_bloque.py` (/* */)

## 3. Elaboración del Autómata Finito Determinista

✅ **Expresión Regular por Token**: Documentadas en `docs/automatas/`

✅ **Dibujo de Autómatas**: Representados con diagramas ASCII en los archivos de documentación

✅ **Autómatas Deterministas**: Todos los autómatas son deterministas, sin ambigüedades en las transiciones

## 3.1 Especificaciones del Analizador Léxico (GUI)

✅ **Ventana con área de texto**: Implementada en la interfaz gráfica

✅ **Botón para análisis léxico**: Implementado como "Analizar Código"

✅ **Tabla de tokens**: Muestra lexema, categoría, fila y columna de cada token

✅ **No uso de expresiones regulares nativas**: Se utilizan exclusivamente ciclos y estructuras de decisión

✅ **Programación carácter a carácter**: Los autómatas procesan el texto carácter por carácter

✅ **Detección de errores**:
   - Cadenas sin cerrar: Detectadas en `analizadores/cadena.py`
   - Tokens no reconocidos: Detectados en `lexer.py`

✅ **No detección de errores sintácticos/semánticos**: El analizador sólo se enfoca en errores léxicos

✅ **Código documentado**: Todas las clases y métodos incluyen comentarios explicativos

## 3.2 Requerimientos no funcionales

✅ **Interfaz clara y ordenada**: Diseño limpio con separación de áreas

✅ **Estándares de programación**:
   - Código comentado
   - Estructuración en múltiples clases
   - Nombres descriptivos para atributos y métodos

✅ **Código en GitHub**: El repositorio es público y accesible

## Extras implementados (no requeridos)

- **Coloreado de tokens**: Los tokens se muestran en diferentes colores según su categoría
- **Botón de limpieza**: Permite resetear el editor y los resultados
- **Manejo de errores mejorado**: Mensajes descriptivos para los errores encontrados
- **Corchetes**: Reconocimiento de corchetes [, ] además de paréntesis y llaves 