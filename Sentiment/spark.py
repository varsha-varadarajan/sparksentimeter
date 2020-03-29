import os, sys
# Path for spark source folder
os.environ['SPARK_HOME'] = "/home/admin/work/spark-1.4.1-bin-hadoop2.4"

# Append pyspark  to Python Path
sys.path.append("/home/admin/work/spark-1.4.1-bin-hadoop2.4/python/")

try:
    from pyspark import SparkContext
    from pyspark import SparkConf

    print ("Successfully imported Spark Modules")
except ImportError as e:
    print ("Can not import Spark Modules", e)
    sys.exit(1)