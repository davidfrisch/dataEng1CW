import pyspark
sc = pyspark.SparkContext('local[*]')

txt = sc.textFile('/mnt/data/DataEng1/coursework/pyspark_example/hello_pyspark.py')
print(txt.count())

python_lines = txt.filter(lambda line: 'python' in line.lower())
print(python_lines.count())