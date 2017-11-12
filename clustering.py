import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import MinMaxScaler
import time


r = open("data/clustering.csv", "w")
r.write("name"+","+"pca_1"+","+"pca_2"+","+"labels"+"\n")
dataset = pd.read_csv("data/features.csv")

name = list(dataset["name"])
X = dataset.drop(["name"], 1)

# Normalization
scaler = MinMaxScaler()
scaler.fit(X)
normal_X = scaler.transform(X)

# PCA
pca = PCA(n_components=2).fit(normal_X)
print(pca.components_)
eigenvalues = pca.explained_variance_ratio_
for e in eigenvalues:
    print("{0:.4f}".format(e))
X_2d = pca.transform(normal_X)

# Dump components relations with features:
#df = pd.DataFrame(pca.components_,columns=X.columns,index = ['PC-1','PC-2','PC-3','PC-4','PC-5','PC-6','PC-7','PC-8'])

#df['MAX']=df.apply(lambda x:x[(x==x.max())].index.to_series().sample(frac=1).iloc[0], axis=1)
#print(df['MAX'])

# kmean clustering
estimator = KMeans(n_clusters=3)

estimator.fit(X_2d)

labels = estimator.labels_

result = []
for n, x, l in zip(name, X_2d, labels):
    x = list(x)
    x.append(l)
    r.write(str(n.lower()) + "," + str(x[0]) + "," +str(x[1])+","+ str(x[2]) +"\n")

r.close()


