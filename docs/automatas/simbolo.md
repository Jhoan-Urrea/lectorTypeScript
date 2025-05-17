# Autómata Finito Determinista para Símbolos y Operadores

## Expresión Regular
No hay una expresión regular única para todos los símbolos, sino varias expresiones para diferentes grupos:

### Operadores Aritméticos
```
[\+\-\*\/%]
```

### Operadores de Comparación
```
(==|===|!=|!==|<|>|<=|>=)
```

### Operadores Lógicos
```
(&&|\|\||!)
```

### Operadores de Asignación
```
(=|\+=|\-=|\*=|\/=|%=)
```

### Operadores de Incremento/Decremento
```
(\+\+|\-\-)
```

### Paréntesis y Llaves
```
[\(\)\{\}]
```

### Terminales y Separadores
```
[;\,\.]
```

### Signos Especiales
```
[\?\:\[\]]
```

### Operadores Especiales de JavaScript
```
(\?\.|\.\.\.|\?\?)
```

## Descripción del Autómata
Debido a la variedad de símbolos y sus combinaciones, el autómata para símbolos es bastante complejo:

- **q0**: Estado inicial
- Estados específicos para cada símbolo o combinación de símbolos
- Estados de aceptación para cada token válido

### Principales grupos de transiciones:
1. **Operadores Aritméticos**: +, -, *, /, %
2. **Operadores de Comparación**: ==, ===, !=, !==, <, >, <=, >=
3. **Operadores Lógicos**: &&, ||, !
4. **Operadores de Asignación**: =, +=, -=, *=, /=, %=
5. **Operadores de Incremento/Decremento**: ++, --
6. **Paréntesis y Llaves**: (, ), {, }
7. **Corchetes**: [, ]
8. **Terminales y Separadores**: ;, ,, .
9. **Operadores Especiales**: ., ?, :, ?., ??, ...

## Diagrama Parcial del Autómata
Debido a la complejidad, mostramos un diagrama simplificado con algunos de los símbolos más comunes:

```
        [+] --> q1 --> [+] --> q2* (++)
      /     \
     /       \--> [=] --> q3* (+=)
    /
   /   [-] --> q4 --> [-] --> q5* (--)
  /     \
 /       \--> [=] --> q6* (-=)
/
q0 --> [*] --> q7 --> [=] --> q8* (*=)
|
|---> [/] --> q9 --> [=] --> q10* (/=)
|
|---> [=] --> q11 --> [=] --> q12* (==)
|                      \
|                       \--> [=] --> q13* (===)
|
|---> [!] --> q14 --> [=] --> q15* (!=)
|                      \
|                       \--> [=] --> q16* (!==)
|
|---> [(] --> q17* (()
|
|---> [)] --> q18* ())
|
|---> [{] --> q19* ({)
|
|---> [}] --> q20* (})
```

*Nota: Los estados con asterisco son estados de aceptación.

## Implementación
El AFD está implementado en `analizadores/simbolo.py`. La implementación:
1. Tiene un método para consumir símbolos carácter por carácter
2. Aplica el principio de máxima coincidencia (ej. reconoce `==` en lugar de solo `=`)
3. Tiene una función para determinar la categoría específica de cada símbolo reconocido
4. No usa expresiones regulares nativas del lenguaje 