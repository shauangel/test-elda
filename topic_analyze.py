import json
import matplotlib.pyplot as plt
import numpy as np


path = "data/models/draw"
file = "/test_result_" + path.split('/')[2] + ".json"

if __name__ == "__main__":
    ##get result
    with open(path+file, "r", encoding="utf-8") as f:
        result = json.load(f)
        f.close()
    c_v = []

    for i in result:
        if (i["c_v"]):
            c_v.append(float(i["c_v"]))
        else:
            c_v.append(0)

    xpoints = np.array(range(0, 90, 10))
    ypoints = np.array(c_v)

    plt.plot(xpoints, ypoints)
    plt.savefig(path.split('/')[2] + ".png")