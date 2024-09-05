import sys
import pandas as pd

print(sys.argv)
day = sys.argv[1]
#something with pandas

print(f'job finished successfully for the day = {day}')
pd.read_csv('/Users/amol/code/learnings/DE/tmp/yellow_tripdata_2019-01.csv', iterator= True, chunksize=100000)