# Autómata Finito Determinista para Comentarios de Bloque

## Expresión Regular
La expresión regular que describe los comentarios de bloque en JavaScript es:

```
\/\*[^*]*\*+([^/*][^*]*\*+)*\/
```

Esta expresión captura:
- Comentarios que empiezan con `/*`
- Cualquier contenido intermedio (incluidos saltos de línea)
- Comentarios que terminan con `*/`

## Descripción del Autómata
El autómata tiene los siguientes estados:
- **q0**: Estado inicial
- **q1**: Después de leer la primera barra (/)
- **q2**: Después de leer asterisco (*) - Inicio del comentario
- **q3**: Leyendo el contenido del comentario
- **q4**: Después de leer asterisco (*) - Posible fin del comentario
- **q5**: Estado de aceptación (después de leer la barra final)

### Transiciones:
- De q0 a q1: Con barra (/)
- De q1 a q2: Con asterisco (*)
- De q2 a q3: Con cualquier carácter excepto asterisco (*)
- De q2 a q4: Con asterisco (*)
- De q3 a q3: Con cualquier carácter excepto asterisco (*)
- De q3 a q4: Con asterisco (*)
- De q4 a q3: Con cualquier carácter excepto barra (/) y asterisco (*)
- De q4 a q4: Con asterisco (*)
- De q4 a q5: Con barra (/)

## Diagrama del Autómata
```
       [/]       [*]                   [*]
  q0 -------> q1 -------> q2 --------------------> q4
                           |                        | ^
                           |                        | |
                           |                        | | [*]
                           |                        | |
                           v        [^*]            v |
                           -------> q3 -------------
                                     ^  |
                                     |  |
                                     |  | [^*]
                                     |  v
                                     ----
                                            [/]
                                     q4 ---------> q5*
```

*Nota: El estado q5 es el único estado de aceptación, representado con un asterisco.

## Implementación
El AFD está implementado en `analizadores/comentario_bloque.py`. La implementación:
1. Reconoce la secuencia inicial "/*"
2. Consume todos los caracteres hasta encontrar la secuencia "*/"
3. Detecta comentarios sin cerrar correctamente
4. No usa expresiones regulares nativas del lenguaje, sino que implementa el autómata carácter por carácter 