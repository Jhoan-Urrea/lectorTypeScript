# Autómata Finito Determinista para Números Naturales

## Expresión Regular
La expresión regular que describe los números naturales en JavaScript es:

```
[0-9]+
```

## Descripción del Autómata
El autómata tiene dos estados:
- **q0**: Estado inicial
- **q1**: Estado de aceptación

### Transiciones:
- De q0 a q1: Con cualquier dígito (0-9)
- De q1 a q1: Con cualquier dígito (0-9)

## Diagrama del Autómata
```
      [0-9]
  q0 --------> q1*
               |  ^
               |  |
               |  | [0-9]
               v  |
               ----
```

*Nota: q1 es un estado de aceptación, representado con el asterisco.

## Implementación
El AFD está implementado en `analizadores/numero_natural.py`. La implementación:
1. Verifica que el primer carácter sea un dígito
2. Continúa consumiendo dígitos mientras los encuentre
3. No usa expresiones regulares nativas del lenguaje, sino que implementa el autómata carácter por carácter 