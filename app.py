from auth import *
import tweepy
import json
import time

auth = tweepy.OAuthHandler(api_key, api_secret_key)
auth.set_access_token(access_token, access_secret_token)
api = tweepy.API(auth, wait_on_rate_limit=True)

flag = False

class MyStreamListener(tweepy.StreamListener):

    def __init__(self, api):
        self.api = api
        self.me = api.me()
        # with open('status.txt', 'w', encoding='utf-8') as file:
        #     file.write('') ### Vider le fichier //TODO : À suppr pour le build
        print("About time...")
    

    def on_status(self,status):

        for tweet in tweepy.Cursor(api.mentions_timeline,nbReplyMax = 1).items():

            # jsonTweet = json.load(tweet)

            with open('oldTweets.json','r') as jsonFile:
                # print('overture r')
                data = json.load(jsonFile)
                for id in data["tweets"]:

                    if id["tweetID"] == tweet.id :
                        flag = True #présent dans le fichier json
                        break
                    else :
                        flag = False #non présent dans le fichier json
                # print(flag)
                jsonFile.close()
                # time.sleep(15)
            if flag == True: continue
            
            with open('oldTweets.json','r+') as jsonFFile:
                # print('ouverture r+')
                if flag == False : 
                    
                    print('2')

                    if tweet.in_reply_to_status_id is None: #le tweet n'est pas un réponse
                        print('pas une réponse')
                        # print(tweet.in_reply_to_status_id)

                        # api.update_status(status = '@<username> Hello there', in_reply_to_status_id = tweet.id)

                        data["tweets"].append({"tweetID" : tweet.id,"userID" : api.get_user(tweet.user.screen_name).id_str, "fullText" : tweet.text})
                        # print("data=",data["tweets"])
                        # print("tweet user ",tweet.user)
                        print(tweet.text)
                        api.update_status('@' + tweet.user.screen_name + ' nice job' , tweet.id)
                        # print(tweet.text)
                        json.dump(data,jsonFFile)   

                    else: #le tweet est un réponse
                        print('erreur')
                        # api.update_status('pas une réponse')

                jsonFile.close()

                    


myStreamListener = MyStreamListener(api)
myStream = tweepy.Stream(api.auth, myStreamListener)
myStream.filter(track=['@WhatAStupidQu']) ### Filtre les tweets à récupérer avec le mot entre ''

        # for x in range(5):
        #     print(status.text) ### Affiche le contenu des tweets au format 'text' dans la console
        #     print('\n##############################################################\n#                         Next Tweet                         #\n##############################################################\n')
        #     with open('status.txt', 'a', encoding='utf-8') as file:
        #         file.write(status.text) ### Écrit les tweets dans le fichier status.txt
        # return False ### Ferme le programme à la fin de la boucle for

# time.sleep(60) ### Attendre 60 sec



# myStream.filter(track=['@WhatAStupidQu']) ### Filtre que tweets qui appelent le wompte en question (WhatAStupidQu)