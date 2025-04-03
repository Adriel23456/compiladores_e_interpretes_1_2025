package com.interprete.ast;

import java.util.Map;

public class OR implements ASTNode{
    private ASTNode operand1;
    private ASTNode operand2;

    public OR(ASTNode operand1, ASTNode operand2) {
        this.operand1 = operand1;
        this.operand2 = operand2;
    }
    @Override
    public Object execute(Map<String, Object> symbolTable) {
        return (boolean) operand1.execute(symbolTable) || (boolean) operand2.execute(symbolTable);
    }
}