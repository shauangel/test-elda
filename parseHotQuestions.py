import requests
import json
from StackData import StackData

url = "https://api.stackexchange.com/2.3/questions?page=2&pagesize=100&order=desc&sort=votes&tagged=python&site=stackoverflow"
file_name = "voteQ_2"

resp = requests.get(url)
data = resp.json()

with open(file_name+"json", "w", encoding='utf-8') as f:
    json.dump(data, f)
    f.close()


with open(file_name+".json", "r", encoding='utf-8') as f:
    data = json.load(f)
    data = data['items']
    f.close()

try:
    with open(file_name+'_full_post.json', 'r', encoding='utf-8') as f:
        result = json.load(f)
        f.close()
except:
    f = open(file_name+'_full_post.json', 'w', encoding='utf-8')
    result = []

#for i in range(0, len(data)):
print(len(data))
for i in range(45, len(data), 5):
    print("No. " + str(i).zfill(3) + "~" + "No. " + str(i+5-1).zfill(3))

    print("parsing...")
    for idx in range(i, i+5):
        print("No. " + str(idx).zfill(3) + ": " + data[idx]['title'])
        parser = StackData(data[idx]['link'])
        result.append(parser.showData())
    #print([data[idx]['link'] for idx in range(i, i+5)])
    #all, q, ans = parseStackData([data[idx]['link'] for idx in range(i, i+5)])

    #result.append(q)
    #result.append(ans)
    with open('voteQ_2_full_post.json', 'w', encoding='utf-8') as f:
        print(len(result))
        json.dump(result, f)
        f.close()
    print("-" * 10)


