'''
Extracting Tweets and it's conversation of particular hashtag using twitter api2.0
'''
from flask import Flask, request, jsonify
from flask_cors import CORS
import datetime
import time
import sys
import requests
import os
import json 
sys.setrecursionlimit(3500)


search_url="https://api.twitter.com/2/tweets/search/recent"

_bearerToken = "YOUR_BEARER_TOKEN"
    # Please enter your bearer token here
bearer_token = _bearerToken


def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


headers = create_headers(bearer_token)


def connect_to_endpoint(url, headers, params):
    # connecting to endpoint and provide response in json format
    response = requests.request("GET", url, headers=headers, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
        #it raises exception if any error occurs while connecting to endpoint
    return response.json()


def list_to_Json(Final_List,File_Name):
    with open('{}.json'.format(File_Name), 'a', encoding='utf8') as file:
        json.dump(Final_List, file, sort_keys=False, indent=4)

def create_url(conversationid):
    # creating url of a particular converstion thread
    return "https://api.twitter.com/2/tweets/search/recent?query=conversation_id:{}".format(conversationid)


def get_params():
    # Tweet fields are adjustable.
    # Options include:
    # attachments, author_id, context_annotations,
    # conversation_id, created_at, entities, geo, id,
    # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
    # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld

    # start = datetime.datetime.strptime("{}T00:00:00Z".format(start_date), "%Y-%m-%dT%H:%M:%SZ").isoformat() + 'Z'
    # end = datetime.datetime.strptime("2022-2-09T00:00:00Z", "%Y-%m-%dT%H:%M:%SZ").isoformat() + 'Z'

    query_params = {
        'tweet.fields': "attachments,author_id,context_annotations,conversation_id,created_at,entities,geo,id,in_reply_to_user_id,lang,possibly_sensitive,public_metrics,referenced_tweets,reply_settings,source,text,withheld",
        'expansions': "attachments.poll_ids,attachments.media_keys,author_id,geo.place_id,in_reply_to_user_id,referenced_tweets.id,entities.mentions.username,referenced_tweets.id.author_id",
        'max_results': 100, 'next_token': next_token}
        # 'end_time': end, 'start_time': start,
    return query_params




def replies(Main_id):
    # It is recursive function for formating replies level wise
    l = []
    for inStance in Conversation_Tweet:
        if 'data' in inStance:
            for values in inStance['data']:
                if (values['referenced_tweets'][0]['id'] == Main_id):
                    # if the replied to id exist and is same as the main id provided while using function then function will repeat itself and form different level
                    # else will return the list of existing level
                    if values['public_metrics']['reply_count'] == 0:
                        v = {"author_id": values['author_id'], "conversation_id": values['conversation_id'],
                            "created_at": values['created_at'], "id": values['id'], "lang": values['lang'],
                            "possibly_sensitive": values['possibly_sensitive'],
                            "public_metrics": values['public_metrics'], "in_reply_to_status_id": values['id'],
                            "referenced_tweets": values['referenced_tweets'],
                            "reply_settings": values['reply_settings'], "source": values['source'],
                            "text": values['text']}
                        l.append(v)
                    else:
                        v = {"author_id": values['author_id'], "conversation_id": values['conversation_id'],
                            "created_at": values['created_at'], "id": values['id'], "lang": values['lang'],
                            "possibly_sensitive": values['possibly_sensitive'],
                            "public_metrics": values['public_metrics'], "in_reply_to_status_id": values['id'],
                            "referenced_tweets": values['referenced_tweets'],
                            "reply_settings": values['reply_settings'], "source": values['source'],
                            "text": values['text'], "replies": replies(values['id'])}
                        l.append(v)

    return l

hash=input("Name hashtag:")
num=int(input("Number of tweets you want"))
repp=input("Replies needed")
lis_Hashtag=[]
lis_Hashtag.append(hash)
#
for i in lis_Hashtag:
    print("{}".format(i))
    #date from where westarted collection of tweets
    #it provides the difference, which we add to start date inorder to move to next date

    # time when the loop begins to run

    next_token = None
    # it is a token to get another set of tweets
    t = True
    conversation_list = []
    # list of coversation id of the main tweet having reply
    conversation_count=0
    # variable that counts total main tweet gathered
    Main_Tweets = []
    # collects all the main tweet
    while t:
        query_params = {'query': '#{} '.format(i),
                        # 'tweet.fields':['id','author_id','text','conversation_id','created_at','lang','context_annotations',
                        #                 'entities','geo','in_reply_to_user_id','non_public_metrics','organic_metrics',
                        #                 'possibly_sensitive','promoted_metrics','public_metrics','referenced_tweets',
                        #                 'reply_settings','source'],
                        'tweet.fields': "attachments,author_id,context_annotations,conversation_id,created_at,entities,geo,id,in_reply_to_user_id,lang,possibly_sensitive,public_metrics,referenced_tweets,reply_settings,source,text,withheld",
                        'expansions': "attachments.poll_ids,attachments.media_keys,author_id,geo.place_id,in_reply_to_user_id,referenced_tweets.id,entities.mentions.username,referenced_tweets.id.author_id",
                        'max_results': 100, 'next_token': next_token}
        try:
            json_response = connect_to_endpoint(search_url, headers, query_params)
            if 'data' in json_response:
                # counts total number of tweet collected till now per day
                conversation_count = conversation_count + json_response['meta']['result_count']
                for j in json_response['data']:
                    # collects the conversation id of those main tweet having replies
                    if j['public_metrics']['reply_count'] != 0:
                        conversation_list.append(j['conversation_id'])
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

        if conversation_count >= num:
            # total tweets we need is 2500 or more hence condition for it
            break
        time.sleep(5)
    list_to_Json(Main_Tweets,"{}_Main_Tweets".format(i))

    if repp=='Y':
        Conversation_Tweet = []
        next_token = None

        n = 0
        for conv_id in conversation_list:
            # loop to get replies from coversation id
            conversationid = conv_id
            url = create_url(conversationid)
            t = True
            print("conversationid:{}".format(n))
            while t:
                params = get_params()
                try:
                    json_response = connect_to_endpoint(url, headers, params)
                except:
                    time.sleep(5)
                    continue
                

                # Conversation_Tweet.append(json_response)
                if 'next_token' in json_response['meta']:
                    next_token = json_response.get('meta').get('next_token')
                else:
                    t = False
                    break
                time.sleep(5)
            n = n + 1
        list_to_Json(Conversation_Tweet,"{}_Conversation_Tweets".format(i))    


        Tweet_replies = []
        # list to formate tweets with replies
        for inStance in Main_Tweets:
            # loop to iterate in main tweets
            if 'data' in inStance:
                for data in inStance['data']:
                    # print(data['possibly_sensitive'])
                    Tweet_replies.append({"author_id": data['author_id'], "conversation_id": data['conversation_id'],
                                            "created_at": data['created_at'], "id": data['id'], "lang": data['lang'],
                                            "possibly_sensitive": data['possibly_sensitive'],
                                            "public_metrics": data['public_metrics'], "text": data['text'],
                                            "replies": replies(data['id']), "source": data['source']})

        list_to_Json(Tweet_replies,"{}".format(i))
    # function which converts tweets with replies in json

#  <!-- {% for i in {{data}} %}
#                 {% for key,values in i.items() %}
#                     {% if {{key}} == "data" %}
#                         {% for j in {{values}} %}
#                             <li>{{j['id']}}--{{j['text']}}--{{j['public_metrics']}}</li>
#                         {%endfor%}
#                     {%endif%}
#                 {%endfor%}
#             {%endfor%}
#              -->