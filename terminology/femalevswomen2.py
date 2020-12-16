import json
import pandas as pd
import numpy as np
import sys
import time

CHUNK_SIZE = 100
BIG_CHUNK_PATH = "D:/datasets/reddit_data/2015/RC_2015-01/RC_2015-01.txt"


def run_analysis():

  # Why is nrows set to that big number you might ask? A bug in pandas. See:
  # https://stackoverflow.com/a/64159741/11319058
  reader = pd.read_json(BIG_CHUNK_PATH, lines=True, chunksize=10000, orient="records", nrows=sys.maxsize)

  chunk_list = []
  # |[^a-zA-Z0-9]girls?[^a-zA-Z0-9]|[^a-zA-Z0-9]boys?[^a-zA-Z0-9]
  regex = "[^a-zA-Z0-9]females?[^a-zA-Z0-9]|[^a-zA-Z0-9]males?[^a-zA-Z0-9]|[^a-zA-Z0-9]wom[ae]n[^a-zA-Z0-9]|[^a-zA-Z0-9]m[ae]n[^a-zA-Z0-9]"
  running_size = 0
  for i, chunk in enumerate(reader):

    #print(chunk)
    #print(chunk['body'].str.contains(regex))
    filtered_chunk = chunk[chunk['body'].str.contains(regex)]
    chunk_list.append(filtered_chunk)
    print(filtered_chunk.body.head(1))

    running_size += filtered_chunk.shape[0]
    print(running_size)

if __name__ == "__main__":
  pd.set_option('display.max_colwidth', None)

  start_time = time.time()
  run_analysis()
  print("--- %s seconds ---" % (time.time() - start_time))
