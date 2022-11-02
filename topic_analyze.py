import json
models_num = [20]
#, 10, 15, 20

for num in models_num:
    with open("test_result_" + str(num) + "_models.json", "r", encoding='utf-8') as f:
        data = json.load(f)
        f.close()

    print(data)