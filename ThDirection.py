#Variables 
tac = []
ssa = []

temp_count = 0
versiones = {}
tac_optimizado = []

#Limpiador
def limpiar_estructuras():
    global tac, ssa, tac_optimizado, temp_count, versiones
    tac.clear()
    ssa.clear()
    tac_optimizado.clear()
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

# OPTIMIZACIONES

def optimizar_tac():
    global tac, tac_optimizado

    codigo = tac.copy()

    codigo = constant_folding(codigo)
    codigo = constant_propagation(codigo)
    codigo = dead_code_elimination(codigo)
    codigo = strength_reduction(codigo)

    # IMPORTANTE:
    # modificar la lista existente
    tac_optimizado.clear()
    tac_optimizado.extend(codigo)

    return tac_optimizado

# CONSTANT FOLDING

def constant_folding(codigo):
    optimizado = []

    for instr in codigo:

        # operaciones: (t1, '=', 2, '+', 3)
        if len(instr) == 5:
            var, eq, izq, op, der = instr

            if isinstance(izq, int) and isinstance(der, int):

                resultado = None

                if op == '+':
                    resultado = izq + der

                elif op == '-':
                    resultado = izq - der

                elif op == '*':
                    resultado = izq * der

                elif op == '/':
                    if der != 0:
                        resultado = izq // der

                elif op == '<':
                    resultado = int(izq < der)

                elif op == '>':
                    resultado = int(izq > der)

                elif op == '<=':
                    resultado = int(izq <= der)

                elif op == '>=':
                    resultado = int(izq >= der)

                elif op == '==':
                    resultado = int(izq == der)

                elif op == '!=':
                    resultado = int(izq != der)

                if resultado is not None:
                    optimizado.append((var, '=', resultado))
                    continue

        optimizado.append(instr)

    return optimizado

# CONSTANT PROPAGATION

def constant_propagation(codigo):

    constantes = {}
    optimizado = []

    for instr in codigo:

        # asignacion simple
        if len(instr) == 3:

            var, eq, val = instr

            if isinstance(val, str) and val in constantes:
                val = constantes[val]

            if isinstance(val, int):
                constantes[var] = val
            else:
                if var in constantes:
                    del constantes[var]

            optimizado.append((var, eq, val))

        # operaciones
        elif len(instr) == 5:

            var, eq, izq, op, der = instr

            if isinstance(izq, str) and izq in constantes:
                izq = constantes[izq]

            if isinstance(der, str) and der in constantes:
                der = constantes[der]

            optimizado.append((var, eq, izq, op, der))

        else:
            optimizado.append(instr)

    return optimizado


# CODIGUIÑO MUERTO

def dead_code_elimination(codigo):

    usadas = set()

    for instr in reversed(codigo):

        # PRINT
        if instr[0] == "PRINT":

            val = instr[1]

            if isinstance(val, str):
                usadas.add(val)

        # IF
        elif instr[0] == "IF":

            cond = instr[1]

            if isinstance(cond, str):
                usadas.add(cond)

        # OPERACIONES
        elif len(instr) == 5:

            var, _, izq, _, der = instr

            if var in usadas:

                if isinstance(izq, str):
                    usadas.add(izq)

                if isinstance(der, str):
                    usadas.add(der)

        # ASIGNACIONES
        elif len(instr) == 3:

            var, _, val = instr

            if var in usadas:

                if isinstance(val, str):
                    usadas.add(val)

    optimizado = []

    for instr in codigo:

        # operaciones
        if len(instr) == 5:

            var = instr[0]

            if var.startswith("t") and var not in usadas:
                continue

        optimizado.append(instr)

    return optimizado


#  REDUCCION

def strength_reduction(codigo):

    optimizado = []

    for instr in codigo:

        if len(instr) == 5:

            var, eq, izq, op, der = instr

            # x * 2  -> x << 1
            if op == '*' and der == 2:
                optimizado.append((var, eq, izq, '<<', 1))
                continue

            # 2 * x -> x << 1
            if op == '*' and izq == 2:
                optimizado.append((var, eq, der, '<<', 1))
                continue

        optimizado.append(instr)

    return optimizado