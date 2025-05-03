import org.apache.spark.SparkConf;
import org.apache.spark.api.java.JavaPairRDD;
import org.apache.spark.api.java.JavaRDD;
import org.apache.spark.api.java.JavaSparkContext;
import scala.Tuple2;

import java.util.Arrays;

public class App {
    public static void main(String[] args) {
        if (args.length < 2) {
            System.err.println("Please provide input and output paths.");
            System.exit(1);
        }
        new App().run(args[0], args[1]);
    }

    public void run(String inputFilePath, String outputDir) {
        SparkConf conf = new SparkConf()
                .setAppName(App.class.getName()); 

        JavaSparkContext sc = new JavaSparkContext(conf);

        JavaRDD<String> textFile = sc.textFile(inputFilePath);

        JavaPairRDD<String, Integer> counts = textFile
                .flatMap(line -> Arrays.asList(line.trim().split("\\s+")).iterator()) 
                .mapToPair(word -> new Tuple2<>(word, 1))
                .reduceByKey(Integer::sum);

        counts.saveAsTextFile(outputDir);

        sc.close();
    }
}
