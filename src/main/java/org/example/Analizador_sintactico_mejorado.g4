grammar Analizador_sintactico_mejorado;

program: PROGRAM ID BRA_OPEN sentence* BRA_CLOSE;

// Lo que puede ser una entada valida
sentence: var_decl | var_assign | println;

var_decl: VAR ID SEMICOLON;

// Ahora acepta expresiones
var_assign: ID ASSIGN expr SEMICOLON;
println: PRINTLN expr SEMICOLON;

// Nueva regla para operaciones matemáticas y lógicas
expr: expr AND expr
    | expr OR expr
    | expr EQ expr
    | expr NEQ expr
    | expr GT expr
    | expr GEQ expr
    | expr LT expr
    | expr LEQ expr
    | expr PLUS expr
    | expr MINUS expr
    | expr MULT expr
    | expr DIV expr
    | NOT expr
    | PAR_OPEN expr PAR_CLOSE
    | NUM
    | ID;

// Saltar espacios en blanco
WS: [ \t\r\n]+ -> skip;

// Palabras clave
PROGRAM: 'program';
VAR: 'var';
PRINTLN: 'println';

// Operadores aritméticos
PLUS: '+';
MINUS: '-';
MULT: '*';
DIV: '/';

// Operadores lógicos
AND: '&&';
OR: '||';
NOT: '!';

NEQ: '!=';
EQ: '==';
GEQ: '>=';
LEQ: '<=';
GT: '>';
LT: '<';

// Asignación
ASSIGN: '=';

// Llaves
BRA_OPEN: '{';
BRA_CLOSE: '}';

// Paréntesis
PAR_OPEN: '(';
PAR_CLOSE: ')';

// Punto y coma
SEMICOLON: ';';

// Identificadores (variables)
ID: [a-zA-Z_][a-zA-Z0-9_]*;

// Números
NUM: [0-9]+;

/* EJEMPLO DE ENTRADA VALIDA
program prueba {
    var x;
    var y;
    x = 10;
    y = 20;
    println(x + y);
    println(x < y && y != 0);
    println((x * 2) >= (y / 2));
}

/*



