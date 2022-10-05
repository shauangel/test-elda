import requests
import json
from StackData import StackData

"""url = "https://api.stackexchange.com/2.3/questions?page=1&pagesize=100&order=desc&sort=votes&tagged=python&site=stackoverflow"

resp = requests.get(url)
data = resp.json()

with open("voteQ.json", "w", encoding='utf-8') as f:
    json.dump(data, f)
    f.close()

"""
with open("voteQ.json", "r", encoding='utf-8') as f:
    data = json.load(f)
    data = data['items']
    f.close()

with open('voteQ_full_post.json', 'r', encoding='utf-8') as f:
    result = json.load(f)
    f.close()

#for i in range(0, len(data)):
for i in range(5, len(data), 5):
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
    with open('voteQ_full_post.json', 'w', encoding='utf-8') as f:
        print(len(result))
        json.dump(result, f)
        f.close()
    print("-" * 10)


