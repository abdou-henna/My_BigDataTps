# TP N°9: Big Data - Apache Spark on Hadoop YARN

This project extends the previous MapReduce TP by integrating **Apache Spark** into our existing Hadoop pseudo-distributed cluster (built with Docker). It demonstrates installing Spark, verifying it works in YARN mode, and running a basic **WordCount Spark job** using `spark-submit`, while leveraging HDFS as input/output data storage.

---

## Step 1: Reuse Existing Docker Hadoop Cluster

We reused the Docker image and 3-container Hadoop cluster created in [TP N°8](../TP8/README.md), which includes:

- A custom image: `hadoop_pseudo`
- Containers:
  * `hadoop-master` (Namenode + ResourceManager)
  * `hadoop-worker1` (Datanode + NodeManager)
  * `hadoop-worker2` (Datanode + NodeManager)

**Image:**  

![Docker Network and Containers](screenshots/docker_network_cluster.png)

---

## Step 2: Install Apache Spark on All Nodes

We installed **Apache Spark 3.5.0** manually inside each container (master and workers). Steps (inside each container):

```bash
cd /opt
wget https://downloads.apache.org/spark/spark-3.5.0/spark-3.5.0-bin-hadoop3.tgz
tar -xvzf spark-3.5.0-bin-hadoop3.tgz
ln -s spark-3.5.0-bin-hadoop3 spark
````

Then we updated `.bashrc`:

```bash
export SPARK_HOME=/opt/spark
export PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin
```

Reload with:

```bash
source ~/.bashrc
```


---

## Step 3: Test Spark with YARN (First Test)

We launched a basic Spark shell test using YARN as the cluster manager:

```bash
spark-shell --master yarn
```

If everything is correctly configured, the shell opens and prints the Spark version and YARN resource messages.

**Image:**

![spark shell result](screenshots/spark_shell_result.png)

---

## Step 4: Create Spark WordCount Java Program

We created a **Java Spark project** using Maven with the following dependency added to `pom.xml`:

```xml
<dependency>
  <groupId>org.apache.spark</groupId>
  <artifactId>spark-core_2.12</artifactId>
  <version>3.5.0</version>
</dependency>
```

The main class `App.java` performs WordCount on a text file stored in HDFS:

```java
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

```

We packaged the project using:

```bash
mvn clean package
```

---

## Step 5: Copy JAR File and Prepare Input in HDFS

We copied the generated JAR to the master node:

```bash
docker cp target/spark-wordcount-1.0-SNAPSHOT.jar hadoop-master:/home/hduser/spark-wordcount.jar
```

Inside `hadoop-master`, we created and uploaded the input text file:

```bash
nano purchases.txt  # Add sample text

hdfs dfs -rm -r /user/root/input
hdfs dfs -mkdir -p /user/root/input
hdfs dfs -put /home/hduser/purchases.txt /user/root/input/
```


---

## Step 6: Execute Spark WordCount with YARN

We ran the job on the Hadoop cluster using:

```bash
hdfs dfs -rm -r /user/root/output

spark-submit \
  --class App \
  --master yarn \
  /home/hduser/spark-wordcount.jar \
  /user/root/input/purchases.txt \
  /user/root/output
```

**Image:**

![spark submit running](screenshots/spark_submit_running.png)


---

## Step 7: View Output from HDFS

After successful execution, we displayed the results from HDFS:

```bash
hdfs dfs -cat /user/root/output/part-*
```

Sample output:

```
(mel,,1)
(duo,2)
(utamur,5)
(mazim,4)
...
```

**Image:**

![job output](screenshots/job_output.png)



### Result Of OurPurchases.txt From Tp08

![our job output](screenshots/our_job_output.png)


---

## Summary

In this TP, we successfully extended our Hadoop Docker cluster from TP8 by installing and configuring **Apache Spark**. We verified the installation using `spark-shell` on YARN, developed a **Java Spark WordCount** program, and executed it in distributed mode using YARN. The successful output in HDFS confirms that Spark jobs are properly running on our cluster.

