import ply.yacc as yacc
from lexer import tokens
from lexer import lexer

errores = []

precedence = (
    ('left', 'MENOR', 'MAYOR', 'MENORIGUAL', 'MAYORIGUAL', 'IGUALIGUAL', 'DIFERENTE'),
    ('left', 'SUMA', 'RESTA'),
    ('left', 'MULTIPLICACION', 'DIVISION'),
)

def p_programa(p):
    '''programa : lista_sentencias
                | empty'''
    p[0] = ("PROGRAMA", p[1])

def p_lista_sentencias(p):
    '''lista_sentencias : lista_sentencias sentencia
                        | sentencia'''
    if len(p) == 3:
        p[0] = ("LISTA", p[1], p[2])
    else:
        p[0] = p[1]

def p_sentencia_asignacion(p):
    '''sentencia : ID IGUAL expresion
                 | ID IGUAL expresion PUNTOYCOMA'''
    p[0] = ("ASIGNACION", p[1], p[3])

def p_sentencia_imprimir(p):
    '''sentencia : IMPRIMIR PARENTESIS_IZQ expresion PARENTESIS_DER
                 | IMPRIMIR PARENTESIS_IZQ expresion PARENTESIS_DER PUNTOYCOMA'''
    p[0] = ("IMPRIMIR", p[3])

def p_expresion_relacional(p):
    '''expresion : expresion MENOR expresion
                 | expresion MAYOR expresion
                 | expresion MENORIGUAL expresion
                 | expresion MAYORIGUAL expresion
                 | expresion IGUALIGUAL expresion
                 | expresion DIFERENTE expresion'''
    p[0] = ("RELACIONAL", p[2], p[1], p[3])

def p_expresion_binaria(p):
    '''expresion : expresion SUMA expresion
                 | expresion RESTA expresion
                 | expresion MULTIPLICACION expresion
                 | expresion DIVISION expresion'''
    p[0] = ("ARITMETICA", p[2], p[1], p[3])

def p_expresion_grupo(p):
    'expresion : PARENTESIS_IZQ expresion PARENTESIS_DER'
    p[0] = p[2]

def p_expresion_numero(p):
    'expresion : NUMERO'
    p[0] = ("NUMERO", p[1])

def p_expresion_id(p):
    'expresion : ID'
    p[0] = ("IDENTIFICADOR", p[1])

def p_expresion_cadena(p):
    'expresion : CADENA'
    p[0] = ("CADENA", p[1])

def p_empty(p):
    'empty :'
    pass

def find_column(input, token):
    last_cr = input.rfind('\n', 0, token.lexpos)
    if last_cr < 0:
        last_cr = -1
    return (token.lexpos - last_cr)

def p_error(p):
    if p:
        columna = find_column(p.lexer.lexdata, p)
        errores.append(f"Error sintáctico en '{p.value}' (línea {p.lineno}, columna {columna})")
    else:
        data = lexer.lexdata  # usar lexer global
        linea = data.count('\n') + 1
        columna = len(data.split('\n')[-1]) + 1

        errores.append(f"Error sintáctico: fin de archivo inesperado (línea {linea}, columna {columna})")


def p_sentencia_imprimir_error(p):
    'sentencia : IMPRIMIR PARENTESIS_IZQ error PARENTESIS_DER'
    print(f"Error: expresión inválida dentro de print en línea {p.lineno(1)}")
    
def p_sentencia_if(p):
    '''sentencia : SI expresion sentencia
                 | SI expresion sentencia SINO sentencia'''
    p[0] = ("IF", p[2], p[3]) if len(p) == 4 else ("IF_ELSE", p[2], p[3], p[5])
        
parser = yacc.yacc()