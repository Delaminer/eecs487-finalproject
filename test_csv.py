import csv


fields = ["original_question", "another_question", "label"]

test=["hahahaha", "zxczxczczx", "0"]
a = [test, test, test]

with open("test.csv", "w") as f:
    csvwriter = csv.writer(f)
    
    csvwriter.writerow(fields)
    csvwriter.writerows(a)


import pandas
df = pandas.read_csv('test.csv')
print(df)

