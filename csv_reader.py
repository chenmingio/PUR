import csv
import re

pattern = r'.*?=\"(.*)\".*'
input_list = []

with open('rfq_part.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
    for row in reader:
        string_list = row[0].split(';')
        row_data = [re.match(pattern, string).group(1) for string in string_list if re.match(pattern, string)]
        input_list.append(row_data)

print(input_list)
print(len(input_list))


