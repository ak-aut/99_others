import discord
import asyncio
import requests
import json
import random
import sqlite3

TOKEN = 'MTAzNjIzMDQ1NTA0Mjc4MTI5OA.GgfSzo.f9J0trjcek6nd0N6athXUEmQWO9f5QKdxdyliQ'

client = discord.Client(intents=discord.Intents.all())

url = "https://script.google.com/macros/s/AKfycbyY3Bol7wFrcyFCk-FIf6oUMn731RkZAglYZd2WoTtZvlc95U81142CVe5rpdpOJnmixw/exec"#もらう

@client.event
async def on_ready():
    print('ready')


@client.event
async def on_message(message):
    if message.author.bot:
        return

    Message_split = message.content.split()

    if Message_split[0] == '/omikuji':##いつかなおす
        if round(random.random()*100)%100 == 1:
            await message.channel.send('博多華丸大吉')
        elif round(random.random()*10)%10 == 1:
            await message.channel.send('大吉')
        elif round(random.random()*10)%10 == 3:
            await message.channel.send('中吉')
        else:
            await message.channel.send('凶')

   
    if Message_split[0] == '/push':
        UserName = Message_split[1]
        json_data = {
            "type" : "addUser",
            "userName" : UserName
        }
        data_encode = json.dumps(json_data)
        f = requests.post(url,data = data_encode)
        await message.channel.send("register success")

    if Message_split[0] == '/list':
        json_data = {
        "type" : "getUserList"
        }
        data_encode = json.dumps(json_data)
        UserList = json.loads(requests.post(url,data = data_encode).text)
        NewUserList = UserList['userList']
        SortedUserList = sorted(NewUserList, key = lambda x : x['rating'], reverse = True) 
        for i in range(len(SortedUserList)):
            if(str(SortedUserList[i]['userName'])[:4] != "TEST"):
                await message.channel.send(str(SortedUserList[i]['userName']) + " : " + str(round(float(SortedUserList[i]['rating']),2)))

    if Message_split[0] == '/listM':
        json_data = {
        "type" : "getUserList"
        }
        data_encode = json.dumps(json_data)
        UserList = json.loads(requests.post(url,data = data_encode).text)
        NewUserList = UserList['userList']
        SortedUserList = sorted(NewUserList, key = lambda x : x['rating'], reverse = True) 
        for i in range(len(SortedUserList)):
            if(SortedUserList[i]['userName'][-1] == 'M'):
                await message.channel.send(str(SortedUserList[i]['userName']) + " : " + str(round(float(SortedUserList[i]['rating']),2)))

    if Message_split[0] == '/redo':
        Result_Users = [0] * (len(Message_split)-1)
        change_rate = [0] * (len(Message_split)-1)
        NewRating = [0] * (len(Message_split)-1)
        for i in range(len(Message_split)-1):
            Result_Users[i] = str(Message_split[i+1])


        json_data_get = {
            "type" : "getRating",
            "users" : Result_Users
        }
        data_encode_get = json.dumps(json_data_get)
        UserRating = json.loads(requests.post(url,data = data_encode_get).text)
        UserName_and_Rating = [{} for i in range(len(Message_split)-1)] ###送る用の二次元配列をなんとかする
        ###複数人のレートの更新法を考える


        for i in range(len(Message_split)-1):
            UserName_and_Rating[i]['userName'] = Message_split[i+1]
            UserName_and_Rating[i]['rating'] = UserRating['ratings'][i]['prevRating']
        json_data_post = {
            "type" : "saveRating",
            "ratings" : UserName_and_Rating
        }
        data_encode_post = json.dumps(json_data_post)
        requests.post(url,data = data_encode_post)
        await message.channel.send("REDO")
        for i in range(len(Result_Users)):
            await message.channel.send(str(UserName_and_Rating[i]['userName']) + " : " + str(round(float(UserName_and_Rating[i]['rating']),2)))

    if Message_split[0] == '/result':
        Result_Users = [0] * (len(Message_split)-1)
        change_rate = [0] * (len(Message_split)-1)
        NewRating = [0] * (len(Message_split)-1)
        for i in range(len(Message_split)-1):
            Result_Users[i] = str(Message_split[i+1])


        json_data_get = {
            "type" : "getRating",
            "users" : Result_Users
        }
        data_encode_get = json.dumps(json_data_get)
        UserRating = json.loads(requests.post(url,data = data_encode_get).text)
        UserName_and_Rating = [{} for i in range(len(Message_split)-1)] ###送る用の二次元配列をなんとかする
        ###複数人のレートの更新法を考える

        for first in range(len(Message_split)-1):
            for second in range(len(Message_split)-1):
                if second <=  first :
                    continue
                P1_rate = float(UserRating['ratings'][first]['rating'])
                P2_rate = float(UserRating['ratings'][second]['rating'])
                W12 = 1/((10 ** ((P1_rate-P2_rate)/400)) + 1)
                change_rate[first] += 32 * W12
                change_rate[second] -= 32 * W12

        for i in range(len(Message_split)-1):
            UserName_and_Rating[i]['userName'] = Message_split[i+1]
            UserName_and_Rating[i]['rating'] = UserRating['ratings'][i]['rating'] + change_rate[i]/(len(Message_split)-2)
        json_data_post = {
            "type" : "saveRating",
            "ratings" : UserName_and_Rating
        }
        data_encode_post = json.dumps(json_data_post)
        requests.post(url,data = data_encode_post)
        await message.channel.send("RESULT")
        for i in range(len(Result_Users)):
            await message.channel.send(str(UserName_and_Rating[i]['userName']) + " : " + str(round(float(UserName_and_Rating[i]['rating']),2)))

    if Message_split[0] == '/resultT':
        Result_Users = [0] * (len(Message_split)-1)
        Number_of_users = (len(Message_split)-1)
        change_rate = [0] * (len(Message_split)-1)
        NewRating = [0] * (len(Message_split)-1)
        for i in range(len(Message_split)-1):
            Result_Users[i] = str(Message_split[i+1])

        first_team_rate = 0
        second_team_rate = 0

        json_data_get = {
            "type" : "getRating",
            "users" : Result_Users
        }
        data_encode_get = json.dumps(json_data_get)
        UserRating = json.loads(requests.post(url,data = data_encode_get).text)
        UserName_and_Rating = [{} for i in range(len(Message_split)-1)] ###送る用の二次元配列をなんとかする
        ###複数人のレートの更新法を考える

        for i in range(len(Message_split)-1):
            if (i < (Number_of_users/2)):
                first_team_rate += float(UserRating['ratings'][i]['rating'])
            else:
                second_team_rate += float(UserRating['ratings'][i]['rating'])

        print(Number_of_users)
        first_team_rate /= (Number_of_users//2)
        second_team_rate /= (Number_of_users//2)
        print(first_team_rate)
        print(second_team_rate)
        W12 = 1/((10 ** ((first_team_rate-second_team_rate)/400)) + 1)

        for i in range(len(Message_split)-1):
            if (i < (Number_of_users/2)):
                change_rate[i] += 32 * W12
            else:
                change_rate[i] -= 32 * W12

        print(change_rate)
        for i in range(len(Message_split)-1):
            UserName_and_Rating[i]['userName'] = Message_split[i+1]
            UserName_and_Rating[i]['rating'] = UserRating['ratings'][i]['rating'] + 2 * change_rate[i]/(len(Message_split)-1)
        json_data_post = {
            "type" : "saveRating",
            "ratings" : UserName_and_Rating
        }
        data_encode_post = json.dumps(json_data_post)
        requests.post(url,data = data_encode_post)
        await message.channel.send("RESULT")
        for i in range(len(Result_Users)):
            await message.channel.send(str(UserName_and_Rating[i]['userName']) + " : " + str(round(float(UserName_and_Rating[i]['rating']),2)))


    if Message_split[0] == '/calc':
        Result_Users = [0] * (len(Message_split)-1)
        change_rate = [0] * (len(Message_split)-1)
        NewRating = [0] * (len(Message_split)-1)
        for i in range(len(Message_split)-1):
            Result_Users[i] = str(Message_split[i+1])

        json_data_get = {
            "type" : "getRating",
            "users" : Result_Users
        }
        data_encode_get = json.dumps(json_data_get)
        UserRating = json.loads(requests.post(url,data = data_encode_get).text)
        UserName_and_Rating = [{} for i in range(len(Message_split)-1)] ###送る用の二次元配列をなんとかする
        ###複数人のレートの更新法を考える

        for first in range(len(Message_split)-1):
            for second in range(len(Message_split)-1):
                if second <=  first :
                    continue
                P1_rate = float(UserRating['ratings'][first]['rating'])
                P2_rate = float(UserRating['ratings'][second]['rating'])
                W12 = 1/((10 ** ((P2_rate-P1_rate)/400)) + 1)
                await message.channel.send('期待勝率：' + str(round(float(W12*100),2)) + '%')

    if Message_split[0] == '/order':
        Result_Users = [0] * (len(Message_split)-1)
        for i in range(len(Message_split)-1):
            Result_Users[i] = str(Message_split[i+1])
        numbers = [0] * 10
        for i in range(10):
            numbers[i] = pow(5,10-i) * pow(4,i)
        Num = {}
        for i in range(len(Message_split)-1):
            Num[i] = random.random() * numbers[i]
        Num2 = sorted(Num.items(), key = lambda x : x[1],reverse = True)
        print(Num2)
        for i in range(len(Num2)):
            await message.channel.send(Result_Users[Num2[i][0]])

    if Message_split[0] == '/randomorder':
        Result_Users = [0] * (len(Message_split)-1)
        for i in range(len(Message_split)-1):
            Result_Users[i] = str(Message_split[i+1])
        numbers = [1] * 10
        Num = {}
        for i in range(len(Message_split)-1):
            Num[i] = random.random() * numbers[i]
        Num2 = sorted(Num.items(), key = lambda x : x[1],reverse = True)
        print(Num2)
        for i in range(len(Num2)):
            await message.channel.send(Result_Users[Num2[i][0]])

client.run(TOKEN)
