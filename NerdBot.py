import telebot
import numpy as np

bot = telebot.TeleBot('8938684986:AAHIgIGzHaImieFfzrRC5-_TY5-YPqb9Y7c')

name = ''
surname = ''
Ira_Score = 23
Dima_Score = 24

answered_questions = [3,45,13]

def chart(update: telebot.Update, context: telebot.CallbackContext) -> None:
    """Send a message with the arguments passed by the user, when the command /chart is issued."""
    input_mex = update.message.text
    input_args = input_mex.split('/chart ')[1]
    update.message.reply_text(input_args)
    
@bot.message_handler(commands=['question'])
def NewQuestion(message):
    send_new_question(message.chat.id)
    
def send_new_question(chat_id):
    available_questions = [
        q for q in range(1, 118)
        if q not in answered_questions
    ]

    if not available_questions:
        bot.send_message(chat_id, "Все вопросы уже были отвечены.")
        return

    new_question = int(np.random.choice(available_questions))
    answered_questions.append(new_question)

    bot.send_message(chat_id, f"Следующий вопрос для нас: {new_question}")
    
@bot.message_handler(commands=['deletequestion'])
def ask_delete_question(message):
    bot.send_message(message.chat.id, "Напиши номер вопроса, который нужно удалить.")
    bot.register_next_step_handler(message, delete_question)


def delete_question(message):
    try:
        question_to_delete = int(message.text)
    except ValueError:
        bot.send_message(message.chat.id, "Нужно ввести число.")
        return

    if question_to_delete not in answered_questions:
        bot.send_message(message.chat.id, f"Мы не отвечали на вопрос {question_to_delete}")
        return

    answered_questions.remove(question_to_delete)

    bot.send_message(
        message.chat.id,
        f"Вопрос {question_to_delete} вычеркнут из списка. Он снова нас ждёт."
    )
    
def add_question(message):
    try:
        question_to_add = int(message.text)
    except ValueError:
        bot.send_message(message.chat.id, "Нужно ввести число.")
        return

    if question_to_add < 1 or question_to_add > 117:
        bot.send_message(message.chat.id, "Номер вопроса должен быть от 1 до 117.")
        return

    if question_to_add in answered_questions:
        bot.send_message(message.chat.id, f"Мы уже отвечали на вопрос {question_to_add}.")
        return

    answered_questions.append(question_to_add)

    bot.send_message(
        message.chat.id,
        f"Вопрос {question_to_add} добавлен в список."
    )
    
@bot.message_handler(commands=['managequestions'])
def ManageQuestions(message):
    if not answered_questions:
        keyboard = telebot.types.InlineKeyboardMarkup()
        
        key_new = telebot.types.InlineKeyboardButton(text='Новый вопрос', callback_data='newquestion')
        keyboard.add(key_new)
        
        #key_delete = telebot.types.InlineKeyboardButton(text='Удалить вопрос', callback_data='deletequestion')    
        #keyboard.add(key_delete)
        
        bot.send_message(message.chat.id, "Пока нет отвеченных вопросов.", reply_markup=keyboard)
        return    
        
    number_string = ", ".join(map(str, answered_questions))
    
    
    keyboard = telebot.types.InlineKeyboardMarkup()
    
    key_new = telebot.types.InlineKeyboardButton(text='Новый вопрос', callback_data='newquestion')
    keyboard.add(key_new)
    
    key_add = telebot.types.InlineKeyboardButton(text='Добавить вопрос', callback_data='addquestion')
    keyboard.add(key_add)
    
    key_delete = telebot.types.InlineKeyboardButton(text='Удалить вопрос', callback_data='deletequestion')    
    keyboard.add(key_delete)
    
    bot.send_message(message.chat.id, text=f"Мы ответили на вопросы: {number_string}", reply_markup=keyboard)
    
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    bot.answer_callback_query(call.id)

    try:
        bot.delete_message(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id
        )
    except Exception as e:
        print("Could not delete message:", e)

    if call.data == "newquestion":
        send_new_question(call.message.chat.id)
        
    elif call.data == "addquestion":
        bot.send_message(
            call.message.chat.id,
            "Напиши номер вопроса, который нужно добавить в список отвеченных."
        )
        bot.register_next_step_handler(call.message, add_question)

    elif call.data == "deletequestion":
        number_string = ", ".join(map(str, answered_questions))

        bot.send_message(
            call.message.chat.id,
            f"Мы ответили на вопросы: {number_string}\nНапиши номер вопроса, который нужно удалить."
        )
        bot.register_next_step_handler(call.message, delete_question)

    elif call.data == 'iraisnerd':
        ira_nerd(call.message.chat.id)

    elif call.data == 'dimaisnerd':
        dima_nerd(call.message.chat.id)

    elif call.data == 'changecount':
        start_nerdness_update(call.message)
        
@bot.message_handler(commands=['info'])
def info_command(message):
    bot.send_message(
        message.chat.id,
        "Бот умеет:\n"
        "/question - Даёт новый вопрос\n"
        "/managequestions - Управление списком вопросов\n"
        "/info - Информация\n"
        "/truth - Узнай истину!\n"
        "/nerdcount - Счёт занудства\n"
        "/nerdness - Изменить счёт занудства\n"
        "/managenerdness - Управление занудством\n"
        "/iranerd - Ира душнит\n"
        "/dimanerd - Не нажимать! Такого не бывает\n"
    )

@bot.message_handler(commands=['truth'])
def help_message(message):
    bot.send_message(message.chat.id, "Ты самая лучшая! Я люблю тебя!")
    
@bot.message_handler(commands=['nerdcount'])
def nerd_count(message):
    print_nerd_count(message.chat.id)
    
def print_nerd_count(chat_id):
    if Ira_Score > Dima_Score:        
        bot.send_message(chat_id, f"Ира ведёт {Ira_Score} против {Dima_Score}! Ты моя любимая зануда :)")
    elif Dima_Score > Ira_Score:
        bot.send_message(chat_id, f"Неожиданно, но Дима ведёт {Dima_Score} против {Ira_Score}! Но это временно)")
    else:
        bot.send_message(chat_id, f"У нас ничья! У обоих по {Dima_Score} очков! Но скоро Ира вырвится вперёд!")

def start_nerdness_update(message):
    global Ira_Score
    global Dima_Score

    bot.send_message(
        message.chat.id,
        f"Счёт занудства:\nИра: {Ira_Score}\nДима: {Dima_Score}"
    )

    bot.send_message(message.chat.id, "Введи счёт Иры:")
    bot.register_next_step_handler(message, nerdness_helper)


@bot.message_handler(commands=['nerdness'])
def manage_nerdness(message):
    start_nerdness_update(message)


def nerdness_helper(message):
    global Ira_Score

    try:
        Ira_Score = int(message.text)
    except ValueError:
        bot.send_message(message.chat.id, "Нужно ввести число. Введи счёт Иры:")
        bot.register_next_step_handler(message, nerdness_helper)
        return

    bot.send_message(message.chat.id, "Введи счёт Димы:")
    bot.register_next_step_handler(message, nerdness_helper_2)


def nerdness_helper_2(message):
    global Dima_Score

    try:
        Dima_Score = int(message.text)
    except ValueError:
        bot.send_message(message.chat.id, "Нужно ввести число. Введи счёт Димы:")
        bot.register_next_step_handler(message, nerdness_helper_2)
        return

    bot.send_message(
        message.chat.id,
        f"Новый счёт:\nИра: {Ira_Score}\nДима: {Dima_Score}"
    )   
            

@bot.message_handler(commands=['iranerd'])
def NerdIra(message):
    ira_nerd(message.chat.id)
    
def ira_nerd(chat_id):
    global Ira_Score
    
    Ira_Score = Ira_Score + 1
    
    bot.send_message(chat_id, f"Ира душнит (ничего нового)! \nТеперь счёт {Ira_Score} против {Dima_Score} у Димы")

@bot.message_handler(commands=['dimanerd'])
def DimaNerd(message):
    dima_nerd(message.chat.id)
    
def dima_nerd(chat_id):
    global Dima_Score
    
    Dima_Score = Dima_Score + 1
    
    bot.send_message(chat_id, f"Дима душнит (неожидынно)! \nТеперь счёт {Dima_Score} против {Ira_Score} у Иры")
    
@bot.message_handler(commands=['managenerdness'])
def ManageNerds(message):      
        
    keyboard = telebot.types.InlineKeyboardMarkup()
    
    key_ira = telebot.types.InlineKeyboardButton(text='Ира душнит!', callback_data='iraisnerd')    
    keyboard.add(key_ira)
    
    key_dima = telebot.types.InlineKeyboardButton(text='Дима душнит!', callback_data='dimaisnerd')    
    keyboard.add(key_dima)
    
    key_count = telebot.types.InlineKeyboardButton(text='Изменить счёт', callback_data='changecount')
    keyboard.add(key_count)   
    
    bot.send_message(message.chat.id, text=f"Счёт занудства: \nИра:{Ira_Score}\nДима{Dima_Score}", reply_markup=keyboard)  

#bot.polling(none_stop=True, interval=0)
bot.infinity_polling()