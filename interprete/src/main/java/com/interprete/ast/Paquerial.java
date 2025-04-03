package com.interprete.ast;
import java.util.Map;

public class Paquerial implements ASTNode{
    private ASTNode operand;

    public Paquerial(ASTNode operand) {
        this.operand = operand;
    }

    @Override
    public Object execute(Map<String, Object> symbolTable) {
        Object value = operand.execute(symbolTable);

        if(!(value instanceof Integer)){
            throw new RuntimeException("Paquerial solo soporta operandos int");
        }
        int n = (Integer) value;
        if(n < 0){
            throw new RuntimeException("No se permite paquerial de números negativos");
        }
        int result = 0;
        while(n > 0){
            result += n;
            n--;
        }
        return  result;
    }
}
