api_key = 'R3xRGpO1yFLT11v9d2N26Qpfz'
api_secret_key = 'NGA2Quoaa0PCE6qcRFwusrKzorrX5lom7VJwvAFZs1vyytUOKU'
access_token = '1413199429004414977-v4Ez8DqS24RuVaXMMKQUeo2OxUWBLn'
access_secret_token = 'ytE1BKs2lNRhxkE7oAl8nbVoJZ7gz6DvXMp6VHfVVb4pL'

import json

def test():
    with open('oldTweets.json','r+') as jsonFile:
        data = json.load(jsonFile)
        for id in data["tweets"]:
            print(id["tweetID"])
        # data[tweets].append(new_data)
        # json.dump(data,jsonFile,indent=4)

# test()