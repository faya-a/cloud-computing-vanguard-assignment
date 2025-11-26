from mrjob.job import MRJob

class WordCount(MRJob):

    def mapper(self, _, line):
        for word in line.split():
            yield word, 1

    def reducer(self, word, values):
        yield word, sum(values)

if __name__ == '__main__':
    WordCount.run()

# python wordcount.py input.txt
# or
# python wordcount.py -r emr s3://bucket/input.txt
