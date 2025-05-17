# Autómata Finito Determinista para Cadenas de Caracteres

## Expresión Regular
La expresión regular que describe las cadenas de caracteres en JavaScript (con comillas dobles, simples o acentos graves) es:

```
("([^"\\]|\\.)*"|'([^'\\]|\\.)*'|`([^`\\]|\\.)*`)
```

Esta expresión captura:
- Cadenas con comillas dobles: `"texto"`
- Cadenas con comillas simples: `'texto'`
- Cadenas con acentos graves (template literals): `` `texto` ``
- Secuencias de escape como `\"`, `\'`, `\``, `\\`, `\n`, `\t`, etc.

## Descripción del Autómata
El autómata tiene los siguientes estados:
- **q0**: Estado inicial
- **q1**: Después de leer comilla doble (")
- **q2**: Después de leer comilla simple (')
- **q3**: Después de leer acento grave (`)
- **q4**: Después de leer barra invertida (\\) en cadena con comillas dobles
- **q5**: Después de leer barra invertida (\\) en cadena con comillas simples
- **q6**: Después de leer barra invertida (\\) en cadena con acentos graves
- **q7**: Estado de aceptación para cadenas con comillas dobles
- **q8**: Estado de aceptación para cadenas con comillas simples
- **q9**: Estado de aceptación para cadenas con acentos graves

### Transiciones:
- De q0 a q1: Con comilla doble (")
- De q0 a q2: Con comilla simple (')
- De q0 a q3: Con acento grave (`)
- De q1 a q1: Con cualquier carácter excepto " y \\
- De q1 a q4: Con barra invertida (\\)
- De q1 a q7: Con comilla doble (")
- De q2 a q2: Con cualquier carácter excepto ' y \\
- De q2 a q5: Con barra invertida (\\)
- De q2 a q8: Con comilla simple (')
- De q3 a q3: Con cualquier carácter excepto ` y \\
- De q3 a q6: Con barra invertida (\\)
- De q3 a q9: Con acento grave (`)
- De q4 a q1: Con cualquier carácter (representa secuencia de escape)
- De q5 a q2: Con cualquier carácter (representa secuencia de escape)
- De q6 a q3: Con cualquier carácter (representa secuencia de escape)

## Diagrama del Autómata
```
                    [^\"\\]
                /------------\
               /             |
              /              |
       ["]   /               |    ["]
  q0 ------>q1 --------------->q7*
       |     \
       |      \
       |       \-->[\\]-->q4-->[cualquier]--
       |                               |    |
       |                               |    |
       |                               -----
       |     [^\'\\]
       |    /------------\
       |   /             |
       |  /              |
       | /               |    [']
       ->q2 --------------->q8*
       |  \
       |   \
       |    \-->[\\]-->q5-->[cualquier]--
       |                               |    |
       |                               |    |
       |                               -----
       |     [^`\\]
       |    /------------\
       |   /             |
       |  /              |
       | /               |    [`]
       ->q3 --------------->q9*
          \
           \
            \-->[\\]-->q6-->[cualquier]--
                                       |    |
                                       |    |
                                       -----
```

*Nota: Los estados q7, q8 y q9 son estados de aceptación, representados con asteriscos.

## Implementación
El AFD está implementado en `analizadores/cadena.py`. La implementación:
1. Reconoce cadenas delimitadas por comillas dobles, simples o acentos graves
2. Maneja secuencias de escape precedidas por barra invertida (\\)
3. Detecta cadenas sin cerrar (un error léxico)
4. No usa expresiones regulares nativas del lenguaje, sino que implementa el autómata carácter por carácter 