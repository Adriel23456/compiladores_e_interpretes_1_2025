grammar interprete;

@parser::header{
    import java.util.Map;
    import java.util.HashMap;
    import com.interprete.ast.ASTNode;
    import com.interprete.ast.Println;
    import com.interprete.ast.If;
    import com.interprete.ast.Addition;
    import com.interprete.ast.Substraction;
    import com.interprete.ast.Multiplication;
    import com.interprete.ast.Divition;
    import com.interprete.ast.Constant;
    import com.interprete.ast.VarDecl;
    import com.interprete.ast.VarAssign;
    import com.interprete.ast.VarRef;
    import com.interprete.ast.Paquerial;
    import com.interprete.ast.MutGen;
}

@parser::members{
    Map <String, Object> symbolTable = new HashMap<String, Object>();
}

program: PROGRAM ID BRACKET_OPEN
    {
        List <ASTNode> body = new ArrayList <ASTNode>();
        Map<String, Object> symbolTable = new HashMap<String, Object>();
    }
 (sentence{body.add($sentence.node);})*
BRACKET_CLOSE
    {
        for(ASTNode n : body){
            n.execute(symbolTable);
        }
    };

sentence returns[ASTNode node]: println {$node = $println.node;}
                                |conditional{$node = $conditional.node;}
                                | var_decl {$node = $var_decl.node;}
                                | var_assign {$node = $var_assign.node;};

println returns [ASTNode node]: PRINTLN expression SEMICOLON
     {$node = new Println($expression.node);};

conditional returns [ASTNode node]: IF PAR_OPEN expression PAR_CLOSE
            {
                List <ASTNode> body = new ArrayList <ASTNode>();
            }
            BRACKET_OPEN
                (s1 = sentence {body.add($s1.node);})*

            BRACKET_CLOSE
          ELSE
          {
                 List <ASTNode> elseBody = new ArrayList <ASTNode>();
          }
            BRACKET_OPEN
                (s2=sentence{elseBody.add($s2.node);})*
            BRACKET_CLOSE
            {
                $node = new If($expression.node, body, elseBody);
            }
            ;

var_decl returns [ASTNode node]:
    VAR ID SEMICOLON {$node = new VarDecl($ID.text);}
    ;
var_assign returns [ASTNode node]:
    ID ASSIGN expression SEMICOLON {$node = new VarAssign($ID.text, $expression.node);}
    ;
expression returns[ASTNode node] :
    t1 = factor {$node = $t1.node;}
        (PLUS t2= factor {$node = new Addition($node, $t2.node);}
        |MINUS t2= factor {$node = new Substraction($node, $t2.node);})*
        |MUTGEN
        PAR_OPEN
            arr = binaryArray
            COMA
            prob = expression
            COMA
            gens = expression
        PAR_CLOSE
        {
            $node = new MutGen($arr.node, $prob.node, $gens.node);
        }
        ;


    factor returns [ASTNode node]:  t1 = comp {$node = $t1.node;}
            (MULT t2= comp {$node = new Multiplication($node, $t2.node);}
            |DIV t2= comp {$node = new Divition($node, $t2.node);})*;
    comp returns [ASTNode node]:
        PAQ term
        {
            $node = new Paquerial ($term.node);
        }
        | PAQ PAR_OPEN expression PAR_CLOSE
        {
            $node = new Paquerial ($expression.node);
        }
        | term
        {
            $node = $term.node;
        }
        ;

term returns [ASTNode node] :
    NUMBER{
        if($NUMBER.text.contains(",") || $NUMBER.text.contains(".")){
            $node = new Constant(Double.parseDouble($NUMBER.text));
        }
        else {
            $node = new Constant(Integer.parseInt($NUMBER.text));
        }
    }
    |BOOLEAN {$node = new Constant(Boolean.parseBoolean($BOOLEAN.text));}
    |ID {$node = new VarRef($ID.text);}
    |PAR_OPEN expression{$node = $expression.node;} PAR_CLOSE;

binaryArray returns [ASTNode node]
  : REC_PAR_OPEN elements+=binaryTerm (COMA elements+=binaryTerm)* REC_PAR_CLOSE
    {
        List<ASTNode> asts = new ArrayList<>();
        // $elements es List<BinaryTermContext>
        for (interpreteParser.BinaryTermContext ctx : $elements) {
            asts.add(ctx.node); // cada ctx tiene su .node
        }
        $node = new Constant(asts);
    }
  ;



binaryTerm returns [ASTNode node]
  : BINARY {
        String bits = $BINARY.text.substring(2); // quitar el prefijo 0b
        $node = new Constant(bits);
    }
  ;



PROGRAM: 'program';
VAR: 'var';
PRINTLN: 'println';
IF: 'if';
ELSE: 'else';

PLUS: '+';
MINUS: '-';
MULT: '*';
DIV: '/';
PAQ: '|-';

AND: '&&';
OR: '||';
NOT: '!';

GT: '>';
LT: '<';
GEQ: '>=';
LEQ: '<=';
NEQ: '!=';

ASSIGN: '=';

BRACKET_OPEN: '{';
BRACKET_CLOSE: '}';

PAR_OPEN: '(';
PAR_CLOSE: ')';

REC_PAR_OPEN: '[';
REC_PAR_CLOSE: ']';

SEMICOLON: ';';
COMA: ',';

BOOLEAN: 'true' | 'false';

MUTGEN: 'mutGen';

ID: [a-zA-Z_][a-zA-Z0-9_]*;
NUMBER:
    [0-9]+ (('.' | ',') [0-9]+)?;
BINARY: '0b' [0-1]+ ;


WS: [ \t\n\r] + -> skip;
