# Autómata Finito Determinista para Palabras Reservadas

## Expresión Regular
No hay una expresión regular única para todas las palabras reservadas, sino una unión de palabras específicas:

```
var|let|const|function|class|if|else|switch|case|default|break|continue|return|while|for|do|new|this|super|delete|typeof|instanceof|void|yield|await|in|of|true|false|null|undefined|try|catch|finally|throw
```

## Descripción del Autómata
Este autómata es de tipo "trie" o árbol de prefijos:
- **q0**: Estado inicial
- Estados intermedios para cada letra de cada palabra reservada
- Estados finales para cada palabra reservada completa

### Transiciones:
- Del estado inicial a los estados que representan la primera letra de cada palabra reservada
- De cada estado intermedio al siguiente según la secuencia de caracteres de la palabra
- Solo se llega a un estado de aceptación si se ha leído una palabra reservada completa

## Diagrama del Autómata
Debido a la complejidad (más de 30 palabras reservadas), el diagrama completo sería muy extenso. Sin embargo, podemos representar una parte simplificada del autómata para algunas palabras clave:

```
                 v --> a --> r --> *
               /
              /
       i --> f --> *
     /
    /         l --> e --> t --> *
   /         /
  /         /    
q0 --------c --> o --> n --> s --> t --> *
  \         \
   \         \
    \         c --> l --> a --> s --> s --> *
     \
      \
       v --> o --> i --> d --> *
```

*Nota: Los estados con asterisco son estados de aceptación.

## Implementación
El AFD está implementado en `analizadores/palabra_reservada.py`. La implementación:
1. Mantiene una lista de palabras reservadas válidas en JavaScript
2. Consume caracteres uno a uno construyendo una posible palabra reservada
3. Verifica que la palabra encontrada esté en la lista de palabras reservadas
4. Verifica que la palabra terminó (no es un prefijo de un identificador más largo)
5. No usa expresiones regulares nativas del lenguaje 