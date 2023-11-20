from pyspark.sql import SparkSession
from time import sleep

# You can find more info in the notion link
# https://www.notion.so/Install-Spark-20825f2589424505b14157a26abc17a8#2ff95e3fd69447fb849a394b0a7cd6dc

def main():
    # Create a Spark session
    spark = SparkSession.builder.appName("ClusterExample").master("spark://ip-10-0-13-106.eu-west-2.compute.internal:7077").getOrCreate()

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