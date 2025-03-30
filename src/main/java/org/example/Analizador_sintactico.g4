// La gramática libre de contexto
grammar Analizador_sintactico;

program: PROGRAM ID BRA_OPEN sentence* BRA_CLOSE;

// Lo que puede ser una entrada valida
sentence: var_decl | var_assign | println;

var_decl: VAR ID SEMICOLON;
var_assign: ID ASSIGN NUM SEMICOLON;
println: PRINTLN (NUM | ID) SEMICOLON;

// Saltar espacios vacios
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
program prueba{
    var a;
    var b;
    a = 100;
    b = 200;
    println a;
    println 1234;
    println b;
}
/*
