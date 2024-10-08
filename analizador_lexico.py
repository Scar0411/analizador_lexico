import ply.lex as lex
from flask import Flask, render_template, request

app = Flask(__name__)

# Palabras reservadas en Java
reserved = {
    'for': 'FOR',
    'while': 'WHILE',
    'if': 'IF',
    'else': 'ELSE',
    'do': 'DO',
    'int': 'INT',
    'float': 'FLOAT',
    'public': 'PUBLIC',
    'static': 'STATIC',
    'void': 'VOID',
    'class': 'CLASS',
    'return': 'RETURN',
    'new': 'NEW'
}

# Lista de tokens incluyendo operadores y símbolos comunes en Java
tokens = [
    'DIGITO', 
    'PUNTO', 
    'PARENTESIS_ABIERTO', 
    'PARENTESIS_CERRADO', 
    'LLAVE_ABIERTA', 
    'LLAVE_CERRADA',
    'PUNTO_Y_COMA', 
    'IDENTIFICADOR', 
    'IGUAL', 
    'OPERADOR_SUMA', 
    'OPERADOR_RESTA', 
    'OPERADOR_MULTIPLICACION',
    'OPERADOR_DIVISION'
    
] + list(reserved.values())

# Expresiones regulares para los tokens
t_DIGITO = r'\d'
t_PUNTO = r'\.'
t_PARENTESIS_ABIERTO = r'\('
t_PARENTESIS_CERRADO = r'\)'
t_LLAVE_ABIERTA = r'\{'
t_LLAVE_CERRADA = r'\}'
t_PUNTO_Y_COMA = r';'
t_IGUAL = r'='
t_OPERADOR_SUMA = r'\+'
t_OPERADOR_RESTA = r'-'
t_OPERADOR_MULTIPLICACION = r'\*'
t_OPERADOR_DIVISION = r'/'
t_ignore = ' \t'

# Identificadores
def t_IDENTIFICADOR(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    if t.value in reserved:
        t.type = reserved[t.value]  # Palabra reservada
    else:
        t.type = 'IDENTIFICADOR'  # Identificador
    return t

# Manejo de nueva línea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Definir el token de error
def t_error(t):
    print('Caracter no válido', t.value[0])
    t.lexer.skip(1)

# Crear el lexer
lexer = lex.lex()

@app.route('/')
def index():
    return render_template('index.html', results=None, code='')

@app.route('/analyze', methods=['POST'])
def analyze():
    text = request.form.get('code', '')
    lexer.input(text)
    
    results = []
    # Analizar el texto línea por línea
    lines = text.splitlines()
    
    for i, line in enumerate(lines, start=1):
        lexer.input(line)
        for token in lexer:
            if token.type in reserved.values():
                category = 'Reservado'
            elif token.type in ['PARENTESIS_ABIERTO', 'PARENTESIS_CERRADO', 'LLAVE_ABIERTA', 'LLAVE_CERRADA', 'PUNTO_Y_COMA']:
                category = 'Delimitador'
            elif token.type in ['OPERADOR_SUMA', 'OPERADOR_RESTA', 'OPERADOR_MULTIPLICACION', 'OPERADOR_DIVISION', 'IGUAL']:
                category = 'Operador'
            elif token.type == 'DIGITO':
                category = 'Número'
            elif token.type == 'PUNTO':
                category = 'Simbolo'
            elif token.type == 'IDENTIFICADOR':
                category = 'Identificador'
            else:
                category = 'Desconocido'
            
            results.append({'token': category, 'lexema': token.value, 'linea': i})
    
    return render_template('index.html', results=results, code=text)

if __name__ == '__main__':
    app.run(debug=True)
