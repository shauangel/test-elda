import json
import re
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

path = "data/exp2/draw/t_5/"
file = "test_result_draw.json"


if __name__ == "__main__":
    with open(path+file, "r", encoding='utf-8')as f:
        result = json.load(f)
        f.close()

    ##target model: best elda models
    target = result[6]

    #scores
    c_v = target['c_v_per_topic']
    #topic top words: top 5
    topic_words = []
    for t in target['070']:
        #p = re.findall(r'(\d*.\d*?)\*', t[1])
        #print(p)
        words = re.findall(r'\*"(.*?)"', t[1])
        topic_words.append("\n".join(words[:5]))
        print(words)
    ##visualize data
    data_topic_score = pd.DataFrame(data=zip(topic_words, c_v), columns=['Topic', 'Coherence'])
    data_topic_score = data_topic_score.set_index('Topic')

    ##matplot
    fig, ax = plt.subplots(figsize=(5, 8))
    ax.set_title("Topics coherence\n $C_v$")
    sns.heatmap(data=data_topic_score, annot=True, square=True,
                cmap='Blues', fmt='.2f',
                linecolor='black', ax=ax)
    plt.yticks(rotation=0)
    ax.set_xlabel('')
    ax.set_ylabel('')

    fig.savefig("test_heat.png")
