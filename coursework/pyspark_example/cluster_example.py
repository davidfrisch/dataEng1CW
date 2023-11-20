from pyspark.sql import SparkSession
from time import sleep

def main():
    # Create a Spark session
    # IP is 100.121.87.128
    spark = SparkSession.builder.appName("ClusterExample").master("spark://" + "1

    # Parallelize a simple dataset
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    rdd = spark.sparkContext.parallelize(data)

    # Perform a simple transformation and action
    computing = rdd.map(lambda x: x * 2)
    sleep(10)
    result = computing.collect()

    # Print the result
    print("Original data:", data)
    print("Transformed data:", result)

    # Stop the Spark session
    spark.stop()

if __name__ == "__main__":
    main()