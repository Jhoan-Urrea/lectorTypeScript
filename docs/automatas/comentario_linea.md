# Autómata Finito Determinista para Comentarios de Línea

## Expresión Regular
La expresión regular que describe los comentarios de línea en JavaScript es:

```
\/\/[^\n]*
```

Esta expresión captura:
- Comentarios que empiezan con `//`
- Todos los caracteres hasta el final de la línea (sin incluir el salto de línea)

## Descripción del Autómata
El autómata tiene los siguientes estados:
- **q0**: Estado inicial
- **q1**: Después de leer la primera barra (/)
- **q2**: Después de leer la segunda barra (/) - Estado de aceptación
- **q3**: Después de leer cualquier carácter que no sea salto de línea - Estado de aceptación

### Transiciones:
- De q0 a q1: Con barra (/)
- De q1 a q2: Con barra (/)
- De q2 a q3: Con cualquier carácter excepto salto de línea (\n)
- De q3 a q3: Con cualquier carácter excepto salto de línea (\n)

## Diagrama del Autómata
```
       [/]       [/]       [^\n]
  q0 -------> q1 -------> q2* -------> q3*
                                       ^  |
                                       |  |
                                       |  | [^\n]
                                       |  v
                                       ----
```

*Nota: Los estados q2 y q3 son estados de aceptación, representados con asteriscos.

## Implementación
El AFD está implementado en `analizadores/comentario_linea.py`. La implementación:
1. Reconoce la secuencia inicial "//"
2. Consume todos los caracteres hasta encontrar un salto de línea o el fin del texto
3. No usa expresiones regulares nativas del lenguaje, sino que implementa el autómata carácter por carácter 