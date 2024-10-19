import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Set;
import java.util.Arrays;
import java.util.stream.Collectors;
public class d3 {
    public static void main(String[] args) throws IOException {
        var total = Files.readAllLines(Path.of("d3.txt")).stream()
            .flatMapToInt(l -> {                
                var l1 = l.substring(0, l.length() / 2).chars().distinct().toArray();    
                return l.substring(l.length() / 2).chars().distinct()
                            .filter(ch -> Arrays.stream(l1).anyMatch(ch1 -> ch1 == ch))
                            .map(x -> (x < 'a') ? (x - 'A' + 27) : (x - 'a' + 1));
            }).sum();
        System.out.printf("Result: %d\n", total);
    }

    private static int i = 0;
    public static void main2(String[] args) throws IOException {
        var total = Files.readAllLines(Path.of("d3.txt")).stream()
            .collect(Collectors.groupingBy(x -> i++ / 3))
            .entrySet().stream()
            .flatMapToInt(l -> 
                l.getValue().stream().map(x -> x.chars().mapToObj(Integer::valueOf).collect(Collectors.toSet()))
                    .reduce((a, b) -> { a.retainAll(b); return a; }).get().stream().mapToInt(x -> x))
            .map(x -> (x < 'a') ? (x - 'A' + 27) : (x - 'a' + 1)).sum();
        System.out.printf("Result: %d\n", total);
    }    
}