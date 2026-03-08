symbol_table = {}

def add_symbol(name, tipo="identificador", valor=None, linea=None):
    if name not in symbol_table:
        symbol_table[name] = {
            "tipo": tipo,
            "valor": valor,
            "linea": linea
        }

def clear_table():
    symbol_table.clear()