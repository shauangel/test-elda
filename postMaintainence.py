import _db
from StackData import StackData

if __name__ == "__main__":
    api = "https://api.stackexchange.com/2.3/questions?page=(page)&pagesize=100&order=desc&sort=votes&tagged=python&site=stackoverflow"

    print("Linking db...")
    all_data = _db.OUTER_DATA_CACHE_COLLECTION.find()
    print("Get post list...")
    parsed = _db.OUTER_DATA_COLLECTION.find()
    print("Check current progress...")
    curr = len([i for i in parsed])
    print("Start parsing...")
    i = 1
    for p in all_data:
        if(i <= curr):
            print(i)
            i+=1
            continue
        else:
            try:
                print(p['title'])
                parser = StackData(p['link'])
                _db.OUTER_DATA_COLLECTION.insert_one(parser.showData())
                i += 1
            except:
                print(i)
                break


# print([data[idx]['link']