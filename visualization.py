import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from collections import Counter


dataset = pd.read_csv("data/clustering.csv")
print(dataset.info())

cls1 = dataset[dataset["labels"]==0]
cls2 = dataset[dataset["labels"]==1]
cls3 = dataset[dataset["labels"]==2]

x_1 = list(cls1["pca_1"])
y_1 = list(cls1["pca_2"])
label_1 = list(cls1["name"])

x_2 = list(cls2["pca_1"])
y_2 = list(cls2["pca_2"])
label_2 = list(cls2["name"])

x_3 = list(cls3["pca_1"])
y_3 = list(cls3["pca_2"])
label_3 = list(cls3["name"])

#scatter
plt.figure()
plt.scatter(x_1, y_1, c="g", marker="o", label="class_1")
#for i, txt in enumerate(label_1):
    #plt.annotate(txt, (x_1[i],y_1[i]))
plt.scatter(x_2, y_2, c="b", marker="*", label="class_2")
for i, txt in enumerate(label_2):
    plt.annotate(txt, (x_2[i],y_2[i]))
plt.scatter(x_3, y_3, c="r", marker="+", label="class_3")
#for i, txt in enumerate(label_3):
#    plt.annotate(txt, (x_3[i],y_3[i]))
plt.legend()


# combine price
price = pd.read_csv("data/Price_Sentiment_url.csv", dtype={"price": np.float64})
price = price.drop(["url","sentiment"], 1)
price["name"] = price["name"].str.lower()

fig, ax = plt.subplots(1,3, figsize=(10, 3))

x_1 = pd.merge(cls1, price, on="name", how="inner")
x_1["cate"] = pd.cut(x_1["price"].values, 3,  labels=["low", "medium", "high"])


ordered_x_1 = x_1.sort_values(["price"], ascending=False)
print("typical coins:", ordered_x_1["name"][:5])
c_1 = dict(Counter(list(x_1["cate"])))
ax[0].pie(c_1.values(), labels=c_1.keys(), autopct='%1.2f%%')
ax[0].set_title("class 1")


x_2 = pd.merge(cls2, price, on="name", how="inner")
x_2["cate"] = pd.cut(x_2["price"].values, 3,  labels=["low", "medium", "high"])
ordered_x_2 = x_2.sort_values(["price"], ascending=False)
print("typical coins:", ordered_x_2["name"][:5])
c_2 = dict(Counter(list(x_2["cate"])))
ax[1].pie(c_2.values(), labels=c_2.keys(), autopct='%1.2f%%')
ax[1].set_title("class 2")


x_3 = pd.merge(cls3, price, on="name", how="inner")
x_3["cate"] = pd.cut(x_3["price"].values, 3,  labels=["low", "medium", "high"])
ordered_x_3 = x_3.sort_values(["price"], ascending=False)
print("typical coins:", ordered_x_3["name"][:5])
c_3 = dict(Counter(list(x_3["cate"])))
ax[2].pie(c_3.values(), labels=c_3.keys(), autopct='%1.2f%%')
ax[2].set_title("class 3")

plt.show()