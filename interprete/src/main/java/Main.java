import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.tree.*;
import java.io.IOException;

public class Main {
    public static void main(String[] args) throws IOException {
        // Ejemplo rápido
        String input = "program miprograma {\n" +
                "var x;\n" +
                "x = 5;" +
                " if (true || false){\n" +
                " println mutGen([0b1010, 0b1100, 0b1111], 0.2, 3);\n" +
                " } else {\n" +
                " println x;\n" +
                "}\n" +
                "}";
        // Crear CharStream
        CharStream cs = CharStreams.fromString(input);

        // Instanciar lexer, parser
        interpreteLexer lexer = new interpreteLexer(cs);
        CommonTokenStream tokens = new CommonTokenStream(lexer);
        interpreteParser parser = new interpreteParser(tokens);

        // Llamar la regla inicial "program"
        interpreteParser.ProgramContext tree = parser.program();

        // Imprimir el árbol de parseo
        System.out.println("Árbol de parseo: " + tree.toStringTree(parser));
    }
}
