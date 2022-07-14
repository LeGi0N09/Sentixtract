import tensorflow as tf
from tensorflow.python.keras.layers import Embedding
from tensorflow.python.keras.layers import LSTM
from tensorflow.python.keras.layers import Dense
import pandas as pd
import numpy as np
import preprocessor as p
# import pickle
import keras.models
import keras 
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
# from keras.models import model_from_json

# https://www.kaggle.com/alankritamishra/covid-19-tweet-sentiment-analysis/data?select=finalSentimentdata2.csv
# File formatting
# df_train
# df_train.drop(["Unnamed: 0"],axis=1,inplace=True)
# df_train.drop(df_train.loc[df_train['label']=="Irrelevant"].index, inplace=True)
# df_train.drop(df_train.loc[df_train['label']=="Neutral"].index, inplace=True)
# df_train
# for ind in df_train.index:
#      if df_train['sentiment'][ind]=="joy":
#        df_train['sentiment'][ind]=1
#      else:
#        df_train['sentiment'][ind]=0
# df_train['sentiment']
# df_train.to_csv("twitter.csv")


voc_size=5000
sent_length=50
embedding_vector_features=40
model=keras.models.Sequential()
model.add(Embedding(voc_size,embedding_vector_features,input_length=sent_length))
model.add(LSTM(100))
model.add(Dense(1,activation='sigmoid'))
model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])
  
cp_callback=tf.keras.callbacks.ModelCheckpoint("cp.ckpt",save_weights_only=True, verbose=1)

rows=[]
df_train = pd.read_csv("twitter.csv")
# 0=Negative
# 1=Positive
print("-------------------------")

X_train = df_train['text']
y_train = df_train['sentiment']

corpus =[p.clean(i) for i in X_train]
onehot_repr=[tf.keras.preprocessing.text.one_hot(str(words),voc_size)for words in corpus]

embedded_docs=tf.keras.preprocessing.sequence.pad_sequences(onehot_repr,padding='pre',maxlen=sent_length)
X=np.array(embedded_docs).astype(np.float32)
y=np.array(y_train).astype(np.float32)
model.fit(X,y_train,epochs=5,validation_split=0.2,batch_size=64)
# Saving the model for Future Inferences
#model.save("my_model.h5")
#,callbacks=[cp_callback]

results = model.evaluate(X, y, batch_size=64)
print("Accuracy: ",results[1]*100)
X_in=input("Enter statement")
corpus1 =[p.clean(X_in)]
pd.DataFrame(corpus1)
onehot_repr1=[tf.keras.preprocessing.text.one_hot(str(words),voc_size)for words in corpus1]
embedded_docs = tf.keras.preprocessing.sequence.pad_sequences(onehot_repr1,padding='pre',maxlen=sent_length)
x=embedded_docs
y=model.predict(x,verbose=0)[0]
if y[0]>0.66:
    print("Positive")
elif y[0]<0.33:
    print("Negative")
else:
    print("Neutral")


# pip install tweet-preprocessor