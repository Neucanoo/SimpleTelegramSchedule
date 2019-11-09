import telebot
import config

bot = telebot.TeleBot(config.token)

def get_groups_keyboard():
    keyboard = telebot.types.InlineKeyboardMarkup()
    count = 0
    while (count < len(config.lessons)):
        count += 5 #groups in row
        if ( len(config.lessons) - count >= 0):
            keyboard.row(
                telebot.types.InlineKeyboardButton( 
                    list(config.lessons)[count - 5], 
                    callback_data = list(config.lessons)[count - 5]
                ),
                telebot.types.InlineKeyboardButton( 
                    list(config.lessons)[count - 4], 
                    callback_data = list(config.lessons)[count - 4]
                ),
                telebot.types.InlineKeyboardButton( 
                    list(config.lessons)[count - 3], 
                    callback_data = list(config.lessons)[count - 3]
                ),
                telebot.types.InlineKeyboardButton( 
                    list(config.lessons)[count - 2], 
                    callback_data = list(config.lessons)[count - 2]
                ),
                telebot.types.InlineKeyboardButton( 
                    list(config.lessons)[count - 1], 
                    callback_data = list(config.lessons)[count - 1]
                )
            )
        elif ( len(config.lessons) - count == -1):
            keyboard.row(
                telebot.types.InlineKeyboardButton( 
                    list(config.lessons)[count - 5], 
                    callback_data = list(config.lessons)[count - 5]
                ),
                telebot.types.InlineKeyboardButton( 
                    list(config.lessons)[count - 4], 
                    callback_data = list(config.lessons)[count - 4]
                ),
                telebot.types.InlineKeyboardButton( 
                    list(config.lessons)[count - 3], 
                    callback_data = list(config.lessons)[count - 3]
                ),
                telebot.types.InlineKeyboardButton( 
                    list(config.lessons)[count - 2], 
                    callback_data = list(config.lessons)[count - 2]
                )
            )
        elif ( len(config.lessons) - count == -2):
            keyboard.row(
                telebot.types.InlineKeyboardButton( 
                    list(config.lessons)[count - 5], 
                    callback_data = list(config.lessons)[count - 5]
                ),
                telebot.types.InlineKeyboardButton( 
                    list(config.lessons)[count - 4], 
                    callback_data = list(config.lessons)[count - 4]
                ),
                telebot.types.InlineKeyboardButton( 
                    list(config.lessons)[count - 3], 
                    callback_data = list(config.lessons)[count - 3]
                )
            )
        elif ( len(config.lessons) - count == -3):
            keyboard.row(
                telebot.types.InlineKeyboardButton( 
                    list(config.lessons)[count - 5], 
                    callback_data = list(config.lessons)[count - 5]
                ),
                telebot.types.InlineKeyboardButton( 
                    list(config.lessons)[count - 4], 
                    callback_data = list(config.lessons)[count - 4]
                )
            )
        elif ( len(config.lessons) - count == -4):
            keyboard.row(
                telebot.types.InlineKeyboardButton( 
                    list(config.lessons)[count - 5], 
                    callback_data = list(config.lessons)[count - 5]
                )
            )
    return keyboard



@bot.message_handler(commands=['start'])
def start_message(message):
    #print userinfo in console
    print("###NewStart###\n", message.from_user, "\n##############")
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row( telebot.types.InlineKeyboardButton('Yep', callback_data = "getgroups") )
    bot.send_message(
        message.chat.id, 
        'Hi. Im schedule bot. Do you want to get a schedule?',
        reply_markup = keyboard
    )



@bot.message_handler(content_types=['text'])
def exchange_command(message):
    if message.text.lower() == u'hi':
        bot.send_message(
            message.chat.id,
            'Hello, choose your group',
            reply_markup = get_groups_keyboard()
        )



@bot.callback_query_handler(func = lambda g: True)
def query_handler(call):
    # call = callback_data
    if call.data == "getgroups": 
        bot.send_message(
            call.from_user.id,
            'Choose group',
            reply_markup = get_groups_keyboard()
        )
        return

    #select day
    if call.data.find("_") == -1: # check if only group in data
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.row( 
            telebot.types.InlineKeyboardButton('Monday', callback_data = call.data + '_1'), 
            telebot.types.InlineKeyboardButton('Thursday', callback_data = call.data + '_4')
        )
        keyboard.row( 
            telebot.types.InlineKeyboardButton('Tuesday', callback_data = call.data + '_2'),
            telebot.types.InlineKeyboardButton('Friday', callback_data = call.data + '_5')
        )
        keyboard.row( 
            telebot.types.InlineKeyboardButton('Wednesday', callback_data = call.data + '_3'),
            telebot.types.InlineKeyboardButton('Saturday', callback_data = call.data + '_6') 
            )
        # call.from_user = info about user
        bot.send_message(
            call.from_user.id,
            'Select day',
            reply_markup = keyboard
        )
        return           
    
    #select week
    if call.data.find("_") != -1 and call.data.find("-") == -1:
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.row( 
            telebot.types.InlineKeyboardButton('First', callback_data = call.data + '-1'),
            telebot.types.InlineKeyboardButton('Second', callback_data = call.data + '-2'), 
        )        
        # call.from_user = info about user
        bot.send_message(
            call.from_user.id,
            'Select week',
            reply_markup = keyboard
        )
        return
    
    #write schedule
    if call.data.find("_") != -1 and call.data.find("-") != -1:
        daypos = call.data.find("_")
        weekpos = call.data.find("-")
        # call.data[0 : daypos] = get group name from data
        # call.data[daypos + 1] = get day
        # call.data[weekpos + 1] = get week
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.row( telebot.types.InlineKeyboardButton('Choose another group', callback_data = "getgroups") )
        keyboard.row( telebot.types.InlineKeyboardButton('Choose another day', callback_data = call.data[0 : daypos]) )
        keyboard.row( telebot.types.InlineKeyboardButton('Choose another week', callback_data = call.data[0 : weekpos]) )
        bot.send_message(
            call.from_user.id, 
            config.lessons[ call.data[0 : daypos] ][ call.data[weekpos + 1] ][ call.data[daypos + 1] ],
            reply_markup = keyboard
        ) 
        #print userinfo in console
        print("##########\n user = ", call.from_user.id, "\n", config.lessons[ call.data[0 : daypos] ][ call.data[weekpos + 1] ][ call.data[daypos + 1] ], "\n" )
        return
        


#Функция polling запускает т.н. Long Polling, а параметр none_stop=True говорит, что бот должен стараться не прекращать работу при возникновении каких-либо ошибок.
if __name__ == '__main__':
    bot.polling(none_stop = True)