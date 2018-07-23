import requests
import random
from datetime import date
import datetime
import statistics
import telebot
from statistics import StatisticsError
def get_age(time_obj): #function to get age from date of burn
    today = date.today() # get today as date
    y = today.year - time_obj.year #get age from subtraction today year and year that man burn
    if today.month < time_obj.month or today.month == time_obj.month and today.day < time_obj.day: #if today month or day lower than month and day of burn we subtract 1 from age
        y -= 1 #subtracting 1
    return y
def mean_age(idi):
    mean_age_id = [] #create list
    mean_age = [] #create list
    age_number = [] #create list
    token = '467a0777d6bcec84a35898eeedcae8a3831ee7329aff982ea2fdaf378c63f2d7ed84e968d94de5a819883' # ---> TOKEN <---
    r_mean_id = requests.get('https://api.vk.com/method/friends.get?user_id='+ str(idi) + '&v=5.52&access_token=' + str(token)) # get id a man for whom we gonna predict age
    json_mean_id = r_mean_id.text #get json as text
    string_mean_id = json_mean_id[34:-3] # get string without useless characters
    mean_ids_list = string_mean_id.split(',') # make list from string with each item as id
    for item in mean_ids_list: # loop through every id in list
        req_mean = requests.get('https://api.vk.com/method/users.get?user_id='+ str(item) + '&v=5.52&access_token=' +str(token) +  '&fields=counters,sex,bdate,country,hometown,lists,last_seen,verified,occupation,wall_comments,can_write_private_message, can_see_audio, can_see_all_posts, can_post')
        # with above line we get request for id in list
        json_mean = req_mean.json() #get json
        for item in json_mean['response']: #get rid of uncomfortable type
            json_dict = item # get json as dict
        while True: #check does a man has birthday
            try:
                age = json_dict['bdate'] # get a birthday if a man has
                break
            except (KeyError, UnboundLocalError) as e: #get rid of error if a man hasn't birthday
                age = '0'
                break
        mean_age.append(age) #add birthday to list
    for item in mean_age: # loop through item in list of birthday
        if len(item) >= 7: # check if len of item more than 7, we do that, because we can have date without year, we don't need that
            dt_obj = datetime.datetime.strptime(item, '%d.%m.%Y') #convert string date to datetime date
            item_number = get_age(dt_obj) # use function get_age to get age from date
            age_number.append(item_number) # add item to list with ages
    first_mean = statistics.mean(age_number) # get mean of list with ages
    age_number = [item for item in age_number if item < first_mean] # get rid of large values that can make our prediction worse
    mean = statistics.mean(age_number) #get mean from list
    return round(mean)
token = '640421091:AAGUXYj-HAwPhZ8g0NvKQn7dO9JOkMw7UZ0'
bot = telebot.TeleBot(token)
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, 'Этот бот может предсказать возраст человека по его странице в вк')

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if message.text.isdigit():
        if len(message.text) < 10:
            while True:
                try:
                    age = mean_age(message.text)
                    bot.reply_to(message, age)
                    break
                except StatisticsError:
                    bot.reply_to(message, 'Простите, но он заплатил нам, чтобы мы удалили его из нашей секретной базы')
                    break
        else:
            bot.reply_to(message, 'Извините, но такого пользователя не существует')
    else:
        bot.reply_to(message, 'введите число')
if __name__ == "__main__":
    while True:
        try:
            bot.infinity_polling(none_stop=True)
        except (Exception,ConnectionResetError,ConnectionError) as e:
            print("Ошибка!!!!\n",str(e))
            logger.error(e)
            time.sleep(15)


