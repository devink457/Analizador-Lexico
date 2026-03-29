#Variables 
tac = []
ssa = []

temp_count = 0
versiones = {}

#Limpiador
def limpiar_estructuras():
    global tac, ssa, temp_count, versiones
    tac.clear()
    ssa.clear()
    temp_count = 0
    versiones.clear()

#Temps
def nueva_temp():
    global temp_count
    temp_count += 1
    return f"t{temp_count}"

#SSA
def nueva_version(var):
    if var not in versiones:
        versiones[var] = 0
    versiones[var] += 1
    return f"{var}{versiones[var]}"

#AST a ATC
def generar_tac(nodo):
    if nodo is None:
        return None

    tipo = nodo[0]

    if tipo == "PROGRAMA":
        generar_tac(nodo[1])

    elif tipo == "LISTA":
        generar_tac(nodo[1])
        generar_tac(nodo[2])

    elif tipo == "ASIGNACION":
        var = nodo[1]
        val = generar_tac(nodo[2])
        tac.append((var, "=", val))
        return var

    elif tipo == "ARITMETICA":
        op = nodo[1]
        izq = generar_tac(nodo[2])
        der = generar_tac(nodo[3])

        temp = nueva_temp()
        tac.append((temp, "=", izq, op, der))
        return temp

    elif tipo == "RELACIONAL":
        op = nodo[1]
        izq = generar_tac(nodo[2])
        der = generar_tac(nodo[3])

        temp = nueva_temp()
        tac.append((temp, "=", izq, op, der))
        return temp

    elif tipo == "NUMERO":
        return nodo[1]

    elif tipo == "IDENTIFICADOR":
        return nodo[1]

    elif tipo == "IMPRIMIR":
        val = generar_tac(nodo[1])
        tac.append(("PRINT", val))

    elif tipo == "IF":
        cond = generar_tac(nodo[1])
        tac.append(("IF", cond))
        generar_tac(nodo[2])

    elif tipo == "IF_ELSE":
        cond = generar_tac(nodo[1])
        tac.append(("IF", cond))
        generar_tac(nodo[2])
        tac.append(("ELSE",))
        generar_tac(nodo[3])

#TAC a SSA
def convertir_a_ssa():
    tabla = {}

    for instr in tac:

        #PRINT
        if instr[0] == "PRINT":
            val = instr[1]
            if val in tabla:
                val = tabla[val]
            ssa.append(("PRINT", val))
            continue

        #IF
        if instr[0] == "IF":
            cond = instr[1]
            if cond in tabla:
                cond = tabla[cond]
            ssa.append(("IF", cond))
            continue

        #ELSE
        if instr[0] == "ELSE":
            ssa.append(instr)
            continue

        #ASIGNACION SIMPLE
        if len(instr) == 3:
            var, _, val = instr

            if val in tabla:
                val = tabla[val]

            nueva = nueva_version(var)
            tabla[var] = nueva

            ssa.append((nueva, "=", val))

        #OPERACION
        elif len(instr) == 5:
            var, _, izq, op, der = instr

            if izq in tabla:
                izq = tabla[izq]
            if der in tabla:
                der = tabla[der]

            nueva = nueva_version(var)
            tabla[var] = nueva

            ssa.append((nueva, "=", izq, op, der))

    return ssa