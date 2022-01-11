import pandas as pd

# get incomplete tasks, add them to a running csv
# tab sep so it's easier to read
# write the name of the file to the scaped logs list.txt

from os import listdir
from os.path import isfile, join
onlyfiles = [f for f in listdir("logs") if isfile(join("logs", f)) & (f[-3:] == "csv")] #get all csv files in logs

for file in onlyfiles:
    df = pd.read_csv("logs/" + file)
    undone = df[df.complete=="n"]
    print(undone[["eventName", "eventDescription"]])
    undone[["eventName", "eventDescription"]].to_markdown("incomplete/testing.md", index=False, tablefmt="grid")
    break

prior_files_scraped = []
with open('logs/scraped_logs_list.txt') as f:
    prior_files_scraped.extend(f.read().splitlines())
print(prior_files_scraped)


# print report metrics



# TODO predict likihood that task is completed in future