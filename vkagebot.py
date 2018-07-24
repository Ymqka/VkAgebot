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
    token = '' # ---> TOKEN <---
    r_mean_id = requests.get('https://api.vk.com/method/friends.get?user_id='+ str(idi) + '&v=5.52&fields=bdate&access_token=' + str(token)) # get id a man for whom we gonna predict age
    json_mean_id = r_mean_id.json() #get json of friends
    if (json_mean_id['response']['count'] != 0):
        for item in json_mean_id['response']['items']:
            if len(item) > 4:
                while True:
                    try:
                        item['bdate']
                        if len(item['bdate']) > 6:
                            age = item['bdate']
                            mean_age.append(age)
                        break
                    except KeyError:
                        break
    for item in mean_age: # loop through item in list of birthday
        if len(item) >= 7: # check if len of item more than 7, we do that, because we can have date without year, we don't need that
            while True:
                try:
                    dt_obj = datetime.datetime.strptime(item, '%d.%m.%Y') #convert string date to datetime date
                    break
                except ValueError:
                    break
            item_number = get_age(dt_obj) # use function get_age to get age from date
            age_number.append(item_number) # add item to list with ages
    first_mean = statistics.mean(age_number) # get mean of list with ages
    age_number = [item for item in age_number if item < first_mean] # get rid of large values that can make our prediction worse
    mean = statistics.mean(age_number) #get mean from list
    return round(mean)
token = ''
bot = telebot.TeleBot(token)
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, 'Этот бот может предсказать возраст человека по его странице в вк.')

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if message.text.isdigit():
        if len(message.text) < 10:
            bot.reply_to(message, 'Это может занять некоторое время.')
            while True:
                try:
                    age = mean_age(message.text)
                    agest = 'Мы считаем что возраст этого человека равен ' + str(age) + ', но мы можем ошибаться на +-1 год.'
                    bot.reply_to(message, agest)
                    break
                except StatisticsError:
                    bot.reply_to(message, 'Простите, но он заплатил нам, чтобы мы удалили его из нашей секретной базы.')
                    break
        else:
            bot.reply_to(message, 'Извините, но такого пользователя не существует.')
    else:
        bot.reply_to(message, 'Введите число.')
if __name__ == "__main__":
    while True:
        try:
            bot.infinity_polling(none_stop=True)
        except (Exception,ConnectionResetError,ConnectionError) as e:
            print("Ошибка!!!!\n",str(e))
            logger.error(e)
            time.sleep(15)
