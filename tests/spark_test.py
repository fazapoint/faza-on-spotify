from pyspark.sql import SparkSession

print("Starting absolute minimum Spark test...")

try:
    # Initialize a basic local Spark session
    spark = SparkSession.builder \
        .appName("MinimalTest") \
        .master("local[*]") \
        .getOrCreate()
    
    print("✅ Success: Spark Session initialized!")
    
    # Create a basic dataframe and compute something
    df = spark.createDataFrame([("Spark is running!",)], ["Status"])
    df.show()
    
    print("✅ Success: Spark successfully processed data!")
    
    # Stop the session cleanly
    spark.stop()
    print("\n🎉 Your local Spark setup is 100% working.")

except Exception as e:
    print("\n❌ Spark failed to start.")
    print(f"Error details:\n{e}")