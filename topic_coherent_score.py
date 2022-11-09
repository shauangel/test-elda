import json

path = "data/exp2/draw/t_5/"
file = "test_result_draw.json"

if __name__ == "__main__":
    with open(path+file, "r", encoding='utf-8')as f:
        result = json.load(f)
        f.close()


