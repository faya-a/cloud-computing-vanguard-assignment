#!/us/bin/sh

hadoop jar hadoop-streaming.jar \
  -input /input \
  -output /output \
  -mapper mapper.py \
  -reducer reducer.py
