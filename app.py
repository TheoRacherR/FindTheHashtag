from auth import *
import tweepy
import json
import datetime
#test2eqo'irgljf
auth = tweepy.OAuthHandler(api_key, api_secret_key)
auth.set_access_token(access_token, access_secret_token)
api = tweepy.API(auth, wait_on_rate_limit=True)

flag = False

class MyStreamListener(tweepy.StreamListener):

    def __init__(self, api):
        self.api = api
        self.me = api.me()
        print("It's show time !")
    

    def on_status(self,status):


        for tweet in tweepy.Cursor(api.mentions_timeline,nbReplyMax = 1).items():

            if tweet.text.startswith('RT @'): 
                print("C'est un RT")
                continue

            hashtag=''
            start=0
            i=0
            idMax=tweet.id
            dateMax=tweet.created_at.date()
            usernameMax=''

            #################################################################################


            with open('oldTweets.json','r') as jsonFile:

                data = json.load(jsonFile)
                for id in data["tweets"]:

                    if id["tweetID"] == tweet.id :
                        flag = True
                        break
                    else :
                        flag = False

                jsonFile.close()

            if flag == True: continue

            # print(flag)

            #################################################################################


            for l in tweet.text:
                if(l == '#'): start = 1
                if(start == 1): hashtag = hashtag + l
                if(start == 1 and l == ' '): break

            if(hashtag == '' or start == 0): continue

            print('hashtag =',hashtag)

            now = datetime.datetime.now()

            print('searching...')
            print(now)

            while(i<1):
                result = api.search(q=hashtag, max_id=idMax)

                try:
                    idMax = result[1].id
                    dateMax = result[1].created_at.date()
                    usernameMax = result[1].user.screen_name
                except:
                    i=1
                    break

                if result[1].text.startswith('RT @'): 
                    continue

            print('idMax =',idMax,'dateMax =',dateMax,'screen_name =',usernameMax)


            now = datetime.datetime.now()
            print('Done.')
            print(now)

            print('fin')
            

            #################################################################################       


            with open('oldTweets.json','r+') as jsonFFile:

                if flag == False : 
                    
                    print('pas une réponse')

                    data["tweets"].append({"tweetID" : tweet.id,"userID" : api.get_user(tweet.user.screen_name).id_str, "fullText" : tweet.text})



                    api.update_status('@' + tweet.user.screen_name + ' Voici le premier tweet pour le hastag ' + hashtag + '\nhttps://twitter.com/' + usernameMax + '/status/'+ str(idMax), tweet.id)

                    json.dump(data,jsonFFile)   


                jsonFile.close()



myStreamListener = MyStreamListener(api)
myStream = tweepy.Stream(api.auth, myStreamListener)
myStream.filter(track=['@SearchForAHT'])
