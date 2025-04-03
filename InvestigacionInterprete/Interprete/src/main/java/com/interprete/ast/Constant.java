package com.interprete.ast;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

public class Constant implements ASTNode{
    private Object value;

    public Constant(Object value) {
        this.value = value;
    }

    @Override
    public Object execute(Map<String, Object> symTable) {
        // Caso especial: si el valor es una lista de nodos (como en [0b1010, 0b1101])
        if (value instanceof List<?>) {
            List<?> list = (List<?>) value;

            // Validar que todos los elementos sean ASTNode
            if (!list.isEmpty() && list.get(0) instanceof ASTNode) {
                List<Object> results = new ArrayList<>();
                for (ASTNode node : (List<ASTNode>) list) {
                    results.add(node.execute(symTable));
                }
                return results; // Devuelve la lista ya evaluada
            }

            return list; // Ya era una lista de valores simples
        }

        // Si no es lista, simplemente devolver el valor (int, double, boolean, string, etc.)
        return value;
    }
}
