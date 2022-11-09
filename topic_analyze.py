import json
import matplotlib.pyplot as plt
import numpy as np


path = "data/models/framework"
file = "/test_result_" + path.split('/')[2] + ".json"

def drawPlot(xPoints, yPoints, name):
    plt.clf()
    plt.plot(xPoints, yPoints, marker=".")
    plt.title = path.split('/')[2] + "_" + name
    plt.xlabel = "topic number"
    plt.ylabel = "coherence score"
    for x, y in zip(xPoints, yPoints):
        plt.text(x, y, y, ha="center", va="bottom", fontsize=8)
    plt.savefig(path + "/" + path.split('/')[2] + "_" + name + ".png")

def vaildFloat(score):
    try:
        num_score = float(score)
    except:
        num_score = 0
    return num_score


if __name__ == "__main__":
    ##get result
    with open(path+file, "r", encoding="utf-8") as f:
        result = json.load(f)
        f.close()
    c_v = []; u_mass = []; c_uci = []; c_npmi = []

    for i in result:
        c_v.append(vaildFloat(i['c_v']))
        u_mass.append(vaildFloat(i['u_mass']))
        c_uci.append(vaildFloat(i['c_uci']))
        c_npmi.append(vaildFloat(i['c_npmi']))

    #display result
    xpoints = np.array(range(10, 100, 10))

    ##u_mass
    drawPlot(xpoints, u_mass, "u_mass")
    ##c_v
    drawPlot(xpoints, c_v, "c_v")
    ##c_uci
    drawPlot(xpoints, c_uci, "c_uci")
    ##c_npmi
    drawPlot(xpoints, c_npmi, "c_npmi")