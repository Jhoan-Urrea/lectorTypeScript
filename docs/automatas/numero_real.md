# Autómata Finito Determinista para Números Reales

## Expresión Regular
La expresión regular que describe los números reales en JavaScript es:

```
([0-9]+\.?[0-9]*|[0-9]*\.[0-9]+)([eE][+-]?[0-9]+)?
```

Esta expresión captura:
- Números enteros (ej. 123)
- Números con parte decimal (ej. 123.45, .5)
- Números en notación científica (ej. 1.23e+4, 5E-3, .5e2)

## Descripción del Autómata
El autómata tiene los siguientes estados:
- **q0**: Estado inicial
- **q1**: Después de leer dígitos (posible estado de aceptación)
- **q2**: Después de leer punto decimal
- **q3**: Después de leer dígitos tras punto decimal (estado de aceptación)
- **q4**: Después de leer 'e' o 'E'
- **q5**: Después de leer signo '+' o '-' en notación científica
- **q6**: Después de leer dígitos en el exponente (estado de aceptación)

### Transiciones:
- De q0 a q1: Con dígitos (0-9)
- De q0 a q2: Con punto decimal (.)
- De q1 a q1: Con dígitos (0-9)
- De q1 a q2: Con punto decimal (.)
- De q1 a q4: Con 'e' o 'E'
- De q2 a q3: Con dígitos (0-9)
- De q3 a q3: Con dígitos (0-9)
- De q3 a q4: Con 'e' o 'E'
- De q4 a q5: Con '+' o '-'
- De q4 a q6: Con dígitos (0-9)
- De q5 a q6: Con dígitos (0-9)
- De q6 a q6: Con dígitos (0-9)

## Diagrama del Autómata
```
                    [0-9]
              /---------------\
              |               |
              v               |
    [0-9]    q1* ---[.]----> q2 
  q0 ----> /   \             |
      \   /     \            | [0-9]
       \ /       \           v
        |         \         q3* <---[0-9]---\
        |          \       /  \              |
        |           \     /    \             |
        |            \   /      \            |
        v             v v        \           |
       [.]          [eE]          \----------/
        |             |
        |             v
        |            q4 -----[+,-]----> q5
        |           /                    |
        |          /                     |
        |         / [0-9]                |
        |        /                       |
        |       v                        v
        \----> q3*                  q6* <---[0-9]---\
                                     ^               |
                                     \---------------/
```

*Nota: Los estados q1, q3 y q6 son estados de aceptación, representados con asteriscos.

## Implementación
El AFD está implementado en `analizadores/numero_real.py`. La implementación:
1. Reconoce números con o sin parte decimal
2. Maneja notación científica con exponente opcional (e+4, E-3, etc.)
3. Permite formatos como .5 (sin dígito antes del punto decimal)
4. No usa expresiones regulares nativas del lenguaje, sino que implementa el autómata carácter por carácter 