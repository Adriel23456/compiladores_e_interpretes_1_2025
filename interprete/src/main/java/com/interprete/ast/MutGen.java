package com.interprete.ast;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Random;

public class MutGen implements ASTNode {

    private final ASTNode arrNode;
    private final ASTNode probNode;
    private final ASTNode gensNode;

    public MutGen(ASTNode arrNode, ASTNode probNode, ASTNode gensNode) {
        this.arrNode = arrNode;
        this.probNode = probNode;
        this.gensNode = gensNode;
    }

    @Override
    public Object execute(Map<String, Object> symTable) {
        Object arrValue = arrNode.execute(symTable);

        // arrValue ya es List<String>
        List<?> nodeList = (List<?>) arrValue;

        List<String> population = new ArrayList<>();
        for (Object obj : nodeList) {
            // "obj" ya es un String binario, no un ASTNode
            population.add(obj.toString());
        }

        // Resto de la lógica (probabilidad, generaciones, mutación) sigue igual
        double p = ((Number) probNode.execute(symTable)).doubleValue();
        int generations = ((Number) gensNode.execute(symTable)).intValue();

        Random rand = new Random();
        List<String> resultado = new ArrayList<>();

        for (String individuo : population) {
            String bits = individuo;
            for (int g = 0; g < generations; g++) {
                StringBuilder mutado = new StringBuilder();
                for (char bit : bits.toCharArray()) {
                    if (rand.nextDouble() < p) {
                        mutado.append(bit == '0' ? '1' : '0');
                    } else {
                        mutado.append(bit);
                    }
                }
                bits = mutado.toString();
            }
            resultado.add(bits);
        }

        for (String r : resultado) {
            System.out.println("Mutado: " + r);
        }

        return resultado;
    }

}
