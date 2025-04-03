package com.interprete.ast;
import java.util.Map;

public class Println implements ASTNode {
    private ASTNode data;

    public Println(ASTNode data) {
        this.data = data;
    }

    @Override
    public Object execute(Map<String, Object> symbolTable) {
        System.out.println(data.execute(symbolTable));
        return null;
    }
}
