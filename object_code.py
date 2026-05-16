codigo_asm = []

variables = set()


def generar_asm(tac):

    codigo_asm.clear()
    variables.clear()

    # =========================
    # SECCIÓN DATA
    # =========================

    codigo_asm.append("section .data")

    # detectar variables
    for instr in tac:

        variables.add(instr[0])

        if len(instr) == 5:

            _, _, op1, _, op2 = instr

            if isinstance(op1, str) and not op1.isdigit():
                variables.add(op1)

            if isinstance(op2, str) and not op2.isdigit():
                variables.add(op2)

        elif len(instr) == 3:

            _, _, valor = instr

            if isinstance(valor, str) and not valor.isdigit():
                variables.add(valor)

    # declarar variables
    for v in variables:
        codigo_asm.append(f"{v} dd 0")

    # =========================
    # SECCIÓN TEXT
    # =========================

    codigo_asm.append("\nsection .text")
    codigo_asm.append("global _start")
    codigo_asm.append("_start:")

    # =========================
    # GENERAR INSTRUCCIONES
    # =========================

    for instr in tac:

        # ==================================
        # OPERACIONES
        # t1 = 1 + 2
        # ==================================

        if len(instr) == 5:

            destino, igual, op1, operador, op2 = instr

            # cargar op1
            if isinstance(op1, int):
                codigo_asm.append(f"mov eax, {op1}")
            else:
                codigo_asm.append(f"mov eax, [{op1}]")

            # operación
            if operador == '+':

                if isinstance(op2, int):
                    codigo_asm.append(f"add eax, {op2}")
                else:
                    codigo_asm.append(f"add eax, [{op2}]")

            elif operador == '-':

                if isinstance(op2, int):
                    codigo_asm.append(f"sub eax, {op2}")
                else:
                    codigo_asm.append(f"sub eax, [{op2}]")

            elif operador == '*':

                if isinstance(op2, int):
                    codigo_asm.append(f"imul eax, {op2}")
                else:
                    codigo_asm.append(f"imul eax, [{op2}]")

            elif operador == '/':

                codigo_asm.append("mov edx, 0")

                if isinstance(op2, int):
                    codigo_asm.append(f"mov ebx, {op2}")
                else:
                    codigo_asm.append(f"mov ebx, [{op2}]")

                codigo_asm.append("idiv ebx")

            # guardar resultado
            codigo_asm.append(f"mov [{destino}], eax")

        # ==================================
        # ASIGNACIONES
        # a = t1
        # ==================================

        elif len(instr) == 3:

            destino, igual, valor = instr

            if isinstance(valor, int):
                codigo_asm.append(f"mov eax, {valor}")
            else:
                codigo_asm.append(f"mov eax, [{valor}]")

            codigo_asm.append(f"mov [{destino}], eax")

    # =========================
    # SALIDA
    # =========================

    codigo_asm.append("\nmov eax, 1")
    codigo_asm.append("int 0x80")

    return codigo_asm


def guardar_asm(codigo):

    with open("programa.asm", "w") as f:

        for linea in codigo:
            f.write(linea + "\n")