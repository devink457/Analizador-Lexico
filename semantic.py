errores_semanticos = []

tabla_valores = {}

def analizar_semantico(arbol):
    errores_semanticos.clear()
    recorrer(arbol)
    return errores_semanticos


def recorrer(nodo):
    if nodo is None:
        return None

    tipo = nodo[0]

    if tipo == "PROGRAMA":
        recorrer(nodo[1])

    elif tipo == "LISTA":
        recorrer(nodo[1])
        recorrer(nodo[2])

    elif tipo == "ASIGNACION":
        nombre = nodo[1]
        valor_tipo = evaluar_expresion(nodo[2])
        tabla_valores[nombre] = valor_tipo

    elif tipo == "IMPRIMIR":
        evaluar_expresion(nodo[1])

    elif tipo == "IF":
        condicion = evaluar_expresion(nodo[1])
        if condicion != "bool":
            errores_semanticos.append("Error: condición de IF no es booleana")
        recorrer(nodo[2])

    elif tipo == "IF_ELSE":
        condicion = evaluar_expresion(nodo[1])
        if condicion != "bool":
            errores_semanticos.append("Error: condición de IF no es booleana")
        recorrer(nodo[2])
        recorrer(nodo[3])


def evaluar_expresion(nodo):
    tipo = nodo[0]

    if tipo == "NUMERO":
        return "int"

    elif tipo == "CADENA":
        return "string"

    elif tipo == "IDENTIFICADOR":
        nombre = nodo[1]
        if nombre not in tabla_valores:
            errores_semanticos.append(f"Error: variable '{nombre}' no definida")
            return "error"
        return tabla_valores[nombre]

    elif tipo == "ARITMETICA":
        op = nodo[1]
        t1 = evaluar_expresion(nodo[2])
        t2 = evaluar_expresion(nodo[3])

        if t1 != "int" or t2 != "int":
            errores_semanticos.append("Error: operación aritmética con tipos no numéricos")
            return "error"

        if op == '/' and nodo[3][0] == "NUMERO" and nodo[3][1] == 0:
            errores_semanticos.append("Error: división entre cero")

        return "int"

    elif tipo == "RELACIONAL":
        t1 = evaluar_expresion(nodo[2])
        t2 = evaluar_expresion(nodo[3])

        if t1 != t2:
            errores_semanticos.append("Error: comparación entre tipos incompatibles")

        return "bool"

    return "error"