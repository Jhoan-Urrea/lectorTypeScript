# Autómata Finito Determinista para Identificadores

## Expresión Regular
La expresión regular que describe los identificadores en JavaScript (limitados a 10 caracteres) es:

```
[a-zA-Z_$][a-zA-Z0-9_$]{0,9}
```

## Descripción del Autómata
El autómata tiene dos estados:
- **q0**: Estado inicial
- **q1**: Estado de aceptación

### Transiciones:
- De q0 a q1: Con letras (a-z, A-Z), guion bajo (_) o signo de dólar ($)
- De q1 a q1: Con letras, dígitos (0-9), guion bajo o signo de dólar
- Se limita la longitud total a un máximo de 10 caracteres

## Diagrama del Autómata
```
      [a-zA-Z_$]
  q0 -----------> q1*
                  |  ^
                  |  |
                  |  | [a-zA-Z0-9_$]
                  v  |
                  ----
```

*Nota: q1 es un estado de aceptación, representado con el asterisco.

## Implementación
El AFD está implementado en `analizadores/identificador.py`. La implementación:
1. Verifica que el primer carácter sea una letra, guion bajo o signo de dólar
2. Luego acepta letras, números, guiones bajos o signos de dólar
3. Se detiene después de consumir 10 caracteres máximo
4. No usa expresiones regulares nativas del lenguaje, sino que implementa el autómata carácter por carácter 