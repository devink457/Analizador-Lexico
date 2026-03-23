import ply.lex as lex
from symbol_table import add_symbol

reservadas = {
    'if': 'SI',
    'else': 'SINO',
    'while': 'MIENTRAS',
    'print': 'IMPRIMIR'
}

tokens = [
    'ID',
    'NUMERO',
    'CADENA',
    'SUMA',
    'RESTA',
    'MULTIPLICACION',
    'DIVISION',
    'IGUAL',
    'MENOR',
    'MAYOR',
    'MENORIGUAL',
    'MAYORIGUAL',
    'IGUALIGUAL',
    'DIFERENTE',
    'PARENTESIS_IZQ',
    'PARENTESIS_DER',
    'PUNTOYCOMA'
] + list(reservadas.values())

t_ignore = ' \t'

# =========================
# OPERADORES ARITMÉTICOS
# =========================
def t_SUMA(t):
    r'\+'
    add_symbol('+', tipo="operador")
    return t

def t_RESTA(t):
    r'-'
    add_symbol('-', tipo="operador")
    return t

def t_MULTIPLICACION(t):
    r'\*'
    add_symbol('*', tipo="operador")
    return t

def t_DIVISION(t):
    r'/'
    add_symbol('/', tipo="operador")
    return t

# =========================
# RELACIONALES
# =========================
def t_MENORIGUAL(t):
    r'<='
    add_symbol('<=', tipo="operador_relacional")
    return t

def t_MAYORIGUAL(t):
    r'>='
    add_symbol('>=', tipo="operador_relacional")
    return t

def t_IGUALIGUAL(t):
    r'=='
    add_symbol('==', tipo="operador_relacional")
    return t

def t_DIFERENTE(t):
    r'!='
    add_symbol('!=', tipo="operador_relacional")
    return t

def t_MENOR(t):
    r'<'
    add_symbol('<', tipo="operador_relacional")
    return t

def t_MAYOR(t):
    r'>'
    add_symbol('>', tipo="operador_relacional")
    return t

# =========================
# ASIGNACIÓN
# =========================
def t_IGUAL(t):
    r'='
    add_symbol('=', tipo="asignacion")
    return t

# =========================
# DELIMITADORES
# =========================
t_PARENTESIS_IZQ = r'\('
t_PARENTESIS_DER = r'\)'
t_PUNTOYCOMA = r';'

# =========================
# LITERALES
# =========================
def t_NUMERO(t):
    r'\d+'
    add_symbol(str(t.value), tipo="numero")
    t.value = int(t.value)
    return t

def t_CADENA(t):
    r'\".*?\"'
    add_symbol(t.value, tipo="cadena")
    return t

# =========================
# IDENTIFICADORES
# =========================
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reservadas.get(t.value, 'ID')
    if t.type == "ID":
        add_symbol(t.value, linea=t.lineno)
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

errores_lexicos = []

def t_error(t):
    mensaje = f"Error léxico: '{t.value[0]}' en línea {t.lineno}"
    errores_lexicos.append(mensaje)
    t.lexer.skip(1)

lexer = lex.lex()