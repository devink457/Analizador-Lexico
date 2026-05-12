codigo_objeto = []

temp_map = {}


def obtener_registro(valor):
    if valor not in temp_map:
        temp_map[valor] = f"R{len(temp_map)+1}"

    return temp_map[valor]


def generar_codigo_objeto(tac):
    codigo_objeto.clear()

    for instruccion in tac:

        # 🔥 OPERACIONES
        if len(instruccion) == 5:

            destino, igual, op1, operador, op2 = instruccion

            r1 = obtener_registro(op1)
            r2 = obtener_registro(op2)
            rd = obtener_registro(destino)

            # mover constantes
            if isinstance(op1, int):
                codigo_objeto.append(f"MOV {r1}, {op1}")

            if isinstance(op2, int):
                codigo_objeto.append(f"MOV {r2}, {op2}")

            if operador == '+':
                codigo_objeto.append(f"ADD {rd}, {r1}, {r2}")

            elif operador == '-':
                codigo_objeto.append(f"SUB {rd}, {r1}, {r2}")

            elif operador == '*':
                codigo_objeto.append(f"MUL {rd}, {r1}, {r2}")

            elif operador == '/':
                codigo_objeto.append(f"DIV {rd}, {r1}, {r2}")

        # 🔥 ASIGNACIONES
        elif len(instruccion) == 3:

            destino, igual, valor = instruccion

            rv = obtener_registro(valor)
            rd = obtener_registro(destino)

            codigo_objeto.append(f"MOV {rd}, {rv}")

    return codigo_objeto