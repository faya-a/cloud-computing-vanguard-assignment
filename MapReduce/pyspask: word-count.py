from pyspark import SparkContext

sc = SparkContext("local", "WordCountDemo")

rdd = sc.textFile("input.txt")

counts = (
    rdd.flatMap(lambda line: line.split())
       .map(lambda word: (word, 1))
       .reduceByKey(lambda a, b: a + b)
)

for word, count in counts.collect():
    print(word, count)
