import preprocessor as p
from flask import Flask, jsonify, render_template, request
from keras.models import load_model
import time
import sys
import requests
import tensorflow as tf
from tensorflow.python.keras.layers import Embedding
from tensorflow.python.keras.layers import LSTM
from tensorflow.python.keras.layers import Dense
import pandas as pd
import numpy as np
import preprocessor as p
import keras.models
import keras
import json 
from textblob import TextBlob
from googleapiclient.discovery import build
sys.setrecursionlimit(3500)

def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers

# def list_to_Json(Final_List,File_Name):
#     with open('../static/{}.json'.format(File_Name), 'a', encoding='utf8') as file:
#         json.dump(Final_List, file, sort_keys=False, indent=4)

def connect_to_endpoint(url, headers, params):
    # connecting to endpoint and provide response in json format
    response = requests.request("GET", url, headers=headers, params=params)
    print(response.status_code)
    # print(response.json)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
        #it raises exception if any error occurs while connecting to endpoint
    return response.json()

# model = load_model('my_model.h5')

def senti(num):
    if num > 0.1:
        return "Positive"
    elif num > -0.1:
        return "Neutral"
    else:
        return "Negative"
    

app = Flask(__name__)

# model = load("my_model.hdf5")

@app.route('/')
def man():
    return render_template('index.html')

@app.route('/form', methods=['GET', 'POST'])
def form():
    # show the form, it wasn't submitted
    return render_template('form.html')

@app.route('/csvfilecreate', methods=['GET', 'POST'])
def csvfilecreate():
    # show the form, it wasn't submitted
    return render_template('csvfilecreate.html')

@app.route('/form_sentiment', methods=['GET', 'POST'])
def form_sentiment():
    # show the form, it wasn't submitted
    return render_template('form_sentiment.html')

@app.route('/apisentiment_form', methods=['GET', 'POST'])
def apisentiment_form():
    # show the form, it wasn't submitted
    return render_template('apisentiment_form.html')

@app.route('/predict', methods=['GET','POST'])
def home():
    data1 = request.form['a']
    voc_size=5000
    sent_length=50
    embedding_vector_features=40
    model=keras.models.Sequential(
        # Embedding(voc_size,embedding_vector_features,input_length=sent_length),
        # LSTM(100),
        # Dense(1,activation='sigmoid'),
    )
    model.add(Embedding(voc_size,embedding_vector_features,input_length=sent_length))
    model.add(LSTM(100))
    model.add(Dense(1,activation='sigmoid'))
    model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])
    
    # cp_callback=tf.keras.callbacks.ModelCheckpoint("cp.ckpt",save_weights_only=True, verbose=1)

    # rows=[]
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
    corpus1 =[p.clean(data1)]
    pd.DataFrame(corpus1)
    onehot_repr1=[tf.keras.preprocessing.text.one_hot(str(words),5000)for words in corpus1]
    embedded_docs = tf.keras.preprocessing.sequence.pad_sequences(onehot_repr1,padding='pre',maxlen=50)
    x=embedded_docs
    pred = model.predict(x,verbose=0)
    return render_template('after.html', data=pred)

@app.route('/extract', methods=['GET','POST'])
def extract():
    data1 = request.form['hashtag']
    data2 = request.form['num']
    next_token = None
    search_url="https://api.twitter.com/2/tweets/search/recent"

    bearer_token = "YOUR_BEARER_TOKEN"
    # Please enter your bearer token here
    headers = create_headers(bearer_token)
# it is a token to get another set of tweets
    t = True
    # list of coversation id of the main tweet having reply
    conversation_count=0
    # variable that counts total main tweet gathered
    Main_Tweets = []
    # collects all the main tweet
    while t:
        query_params = {'query': '#{} lang:en'.format(data1),
                        # 'tweet.fields':['id','author_id','text','conversation_id','created_at','lang','context_annotations',
                        #                 'entities','geo','in_reply_to_user_id','non_public_metrics','organic_metrics',
                        #                 'possibly_sensitive','promoted_metrics','public_metrics','referenced_tweets',
                        #                 'reply_settings','source'],
                        'tweet.fields': "id,public_metrics,text",
                        'max_results': 100, 'next_token': next_token}
        try:
            json_response = connect_to_endpoint(search_url, headers, query_params)
            if 'data' in json_response:
                # counts total number of tweet collected till now per day
                conversation_count = conversation_count + json_response['meta']['result_count']
        except:
            time.sleep(5)
            continue
        Main_Tweets.append(json_response)
        if 'next_token' in json_response['meta']:
            # if there are more than 100 tweets it will have next token which helps us to collect following 100 tweets
            next_token = json_response['meta']['next_token']

        else:
            t = False
            break

        if conversation_count >= int(data2):
            # total tweets we need is 2500 or more hence condition for it
            break
        time.sleep(5)
    
    # result=json.dumps(Main_Tweets)
    return render_template('extracted_tweet.html',data=Main_Tweets)

@app.route('/perspective', methods=['GET', 'POST'])
def perspective():
    data1 = request.form['a']
    API_KEY = 'YOUR_API_KEY'
    # Please enter your googple perspective api token here 
    # result = TextBlob(data1)
    # pred=result.sentiment.polarity
    client = build(
    "commentanalyzer",
    "v1alpha1",
    developerKey=API_KEY,
    discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
    )

    analyze_request = {
    'comment': { 'text': '{}'.format(data1) },
    'requestedAttributes': {'TOXICITY': {},'INSULT':{},'PROFANITY':{},'THREAT':{},'IDENTITY_ATTACK':{}}
    }

    response = client.comments().analyze(body=analyze_request).execute()
    # has 60 queries per min
    pred = {
        'Text':analyze_request['comment']['text'],
            'Toxicity': response['attributeScores']['TOXICITY']['spanScores'][0]['score']['value'],
            'Insult' :response['attributeScores']['INSULT']['spanScores'][0]['score']['value'],
            'Profanity':response['attributeScores']['PROFANITY']['spanScores'][0]['score']['value'],
            'Threat':response['attributeScores']['THREAT']['spanScores'][0]['score']['value'],
            'IDENTITY_ATTACK':response['attributeScores']['IDENTITY_ATTACK']['spanScores'][0]['score']['value']
            }
    print(pred)
    return render_template('after_api.html', data=pred)

@app.route('/csv_file', methods=['GET', 'POST'])
def csv_file():
    data1 = request.form['hashtag']
    data2 = request.form['num']
    next_token = None
    search_url="https://api.twitter.com/2/tweets/search/recent"

    bearer_token = "YOUR_BEARER_TOKEN"
    # Please enter your bearer token here
    headers = create_headers(bearer_token)
# it is a token to get another set of tweets
    t = True
    # list of coversation id of the main tweet having reply
    conversation_count=0
    # variable that counts total main tweet gathered
    Main_Tweets = []
    # collects all the main tweet
    while t:
        query_params = {'query': '#{} lang:en'.format(data1),
                        # 'tweet.fields':['id','author_id','text','conversation_id','created_at','lang','context_annotations',
                        #                 'entities','geo','in_reply_to_user_id','non_public_metrics','organic_metrics',
                        #                 'possibly_sensitive','promoted_metrics','public_metrics','referenced_tweets',
                        #                 'reply_settings','source'],
                        'tweet.fields': "author_id,public_metrics,text",
                        'max_results': 100, 'next_token': next_token}
        try:
            json_response = connect_to_endpoint(search_url, headers, query_params)
            if 'data' in json_response:
                # counts total number of tweet collected till now per day
                conversation_count = conversation_count + json_response['meta']['result_count']
        except:
            time.sleep(5)
            continue
        for i in json_response['data']:
            Main_Tweets.append(i)

        if 'next_token' in json_response['meta']:
            # if there are more than 100 tweets it will have next token which helps us to collect following 100 tweets
            next_token = json_response['meta']['next_token']
        else:
            t = False
            break

        if conversation_count >= int(data2):
            # total tweets we need is 2500 or more hence condition for it
            break
        time.sleep(5)
    # print(Main_Tweets)

    for i in Main_Tweets:
        # TextBlob(j["text"]).sentiment.polarity senti(TextBlob(j["text"]).sentiment.polarity)
        i['sentiment_score'] = TextBlob(i["text"]).sentiment.polarity
        i['sentiment'] = senti(TextBlob(i["text"]).sentiment.polarity)
        # print(i.text)
        # print(type(i))

    csvdata = {"data":Main_Tweets}

    return render_template('csv_file.html', data=csvdata)

if __name__ == "__main__":
    app.run(debug=True)




# <!-- {%if data > (0.33) %}
#     <h1>Positive</h1>  
#     <img src="{{url_for('static', filename='sentiment-analysis2.png')}}" alt="Positive analysis">

#     {%else %}
#         {% if data > (-0.33) %}
#         <h1>Neutral</h1>
#         <img src="{{url_for('static', filename='sentiment-analysis3.png')}}" alt="Neutral analysis"> 

#         {%else %}
#         <h1>Negative</h1>
#         <img src="{{url_for('static', filename='sentiment-analysis1.png')}}" alt="Negative analysis">
#         {%endif%}
#     {%endif%} -->