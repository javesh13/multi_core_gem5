# In[1]:


from sklearn.cluster import KMeans
import pandas as pd, numpy as np
from matplotlib import pyplot as plt
from collections import Counter
from sklearn.metrics import silhouette_score
import math

from keras import Model
from keras.layers import LSTM, Input, Dense, Concatenate, Embedding, Dropout
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.optimizers import SGD
from keras.models import load_model
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder
from collections import Counter
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OrdinalEncoder


import os
os.environ['CUDA_VISIBLE_DEVICES'] = "0"

print("Physical devices:" ,tf.config.list_physical_devices('GPU'))


# ## Constants
# 

# In[2]:


batch_size = 100
debug  =0


# In[16]:


import pickle

f = open("./401_data/ohe_401", "rb")
ohe_401 =  pickle.load(f)

ohe_401.handle_unknown="ignore"
f.close()

f = open("./429_data/ohe_429", "rb")
ohe_429 =  pickle.load(f)
ohe_429.handle_unknown="ignore"
f.close()


# In[22]:



# train=600000
df_for_training = pd.read_csv('delta_augumented_file.csv', nrows=2000000)#reading only PC and Delta
cols = df_for_training.columns
df_for_training = df_for_training[cols].astype(float)
cols = df_for_training.columns



df0 = df_for_training[df_for_training['cpu'] == 0]
df1 = df_for_training[df_for_training['cpu'] == 1]




dfs = [df0, df1]
print(df_for_training.shape)
oe_PCs = []
oe_Deltas = []

for i in range(2):

    MAX_DELTA = int(dfs[i]['Delta'].nunique()) + 1
    MAX_PC = int(dfs[i]['PC'].nunique()) + 1


    oe_PC = OrdinalEncoder()
    oe_Delta = OrdinalEncoder()

    oe_PC = oe_PC.fit(dfs[i]['PC'].values.reshape(-1, 1))
    oe_Delta = oe_Delta.fit(dfs[i]['Delta'].values.reshape(-1, 1))

    oe_PCs.append(oe_PC)
    oe_Deltas.append(oe_Delta)


# In[23]:


model0 = load_model("./401_data/best_model_401.h5")
model1 = load_model("./429_data/best_model_429.h5")


# In[43]:





models =  [model0, model1]
# df  = pd.read_csv("delta_augumented_file.csv", nrows=4000000)
#we have PC,Cache,Delta,CPU
hit_0 = 0
hit_1 = 0


q0 = []
q1 = []

oe_PC_401 = oe_PCs[0]
oe_PC_429 = oe_PCs[1]

oe_Delta_401 = oe_Deltas[0]
oe_Delta_429 = oe_Deltas[1]


def process_vals(vals):
    pc = vals[0]
    cache = vals[1]
    delta  = vals[2]
    if(vals[-1] == 0):
        pc = oe_PC_401.transform([[pc]])
        delta_t = oe_Delta_401.transform([[delta]])
        q0.append((pc[0][0], delta_t[0][0], delta))
        do_predict(0)
    else:
        pc = oe_PC_429.transform([[pc]])
        delta_t = oe_Delta_429.transform([[delta]])
        q1.append((pc[0][0], delta_t[0][0], delta))
        do_predict(1)


def do_predict(cpu):
    global q0, q1, hit_0, hit_1
    if(cpu == 0):
        if(len(q0) == 21):
            q = q0[0:20]
            q = [(x[0], x[1]) for x in q]

            xs = np.array(q[0:20])

            y = np.array([[q0[20:21][0][2]]]) 

            pcs = [a[0] for a in xs]
            deltas_t = [a[1] for a in xs]

            # od = oe_Delta_401.inverse_transform(y)
            y_true = ohe_401.transform(y).argmax()


            y_predicted = models[0].predict([[pcs], [deltas_t]])
            y_predicted = y_predicted.argmax()
            if(y_true == y_predicted):
                hit_0+=1
            q0 = q0[1:]
    else:
        if(len(q1) == 21):
            q = q1[0:20]
            q = [(x[0], x[1]) for x in q]   

            xs = np.array(q[0:20])

            y = np.array([[q1[20:21][0][2]]]) 

            pcs = [a[0] for a in xs]
            deltas_t = [a[1] for a in xs]

            # od = oe_Delta_401.inverse_transform(y)
            y_true = ohe_401.transform(y).argmax()


            y_predicted = models[0].predict([[pcs], [deltas_t]])
            y_predicted = y_predicted.argmax()
            if(y_true == y_predicted):
                hit_1+=1
            q1 = q1[1:]
            

with open("delta_augumented_file.csv") as f:
    head = [next(f) for x in range(2000001)]

print("Total Lines: ", len(head))
line_count = 0
for line in head:
    if "PC" in line:
        continue
    vals = list(map(int, line.strip().split(",")))
    # print(vals)
    process_vals(vals)
    print("Line Count: {}, Hit0: {}, Hit1: {}".format(line_count,hit_0, hit_1), end="\r")
    line_count += 1
        


