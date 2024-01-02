
import os

absolute_path = os.path.dirname(__file__)
FILE_PATH = os.path.join(absolute_path, '../site_list/jasminedirectory.csv')

fin_set = set()

for file_name in list(map(lambda x: 'jasminedirectory_'+chr(x)+'.csv', range(97, 123))):
    with open(os.path.join(absolute_path, '../site_list/'+file_name), 'r') as f:
        for line in f:
            fin_set.add(line)
        f.close()

with open(FILE_PATH, 'w+') as f:
    for line in fin_set:
        f.write(line)
    f.close()
