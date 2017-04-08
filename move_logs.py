import codecs
import datetime
import os

f_path = os.path.expanduser('~') + "/.ncdc/stderr.log"

lines = []

with codecs.open(f_path, 'r', encoding='utf-8', errors='ignore') as f:
    for line in f:
        if '$Search' in line:
            lines.append(line.split())

now = datetime.datetime.now()
target_path = "/home/hunter/workspace/dctrends/data/" + now.strftime('%Y-%m-%d %H:00')

to_append = ""
for item in lines:
    if 'TTH:' in item[-1]:
        continue
    query = '{date} {time} {ip} "{terms}"\n'
    date = item[0].lstrip('[')
    ip = item[6].split(':')[0]
    if 'Invalid' in item[5] or '$Search' in ip:
        continue
    terms = item[-1].split('?')[-1].replace('$', ' ').rstrip('|')
    query = query.format(date=date, time=item[1], ip=ip, terms=terms)
    # print("len query", len(query))
    # print("query ", query)
    to_append += query

with open(target_path, 'a') as f:
    f.write(to_append)

print(len(lines), " New search queries.")
