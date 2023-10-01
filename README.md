# Бот-викторина! 
чат-бот с каверзными вопросами и единственным правильным вариантом ответа. Кто победит – того и приз.

![Пример работы](https://github.com/Pavel2232/BotForQuiz/blob/master/examination_tg.gif)
# [Бот Тг](https://t.me/QuizPabloBot)
![](https://github.com/Pavel2232/BotForQuiz/blob/master/examination_vk.gif)
# [Бот Вк](https://vk.com/club222012081)
### Как запустить проект.
1. ``` git clone https://github.com/Pavel2232/BotForQuiz```

2. Установите необходимые библиотеки  ```poetry install```

3. Создайте файл .env и заполните следующие значения:
* TG_BOT_TOKEN=ключ телеграм бота 
* VK_BOT_TOKEN=ключ вк бота
* VK_CHAT_ID=ваш чат айди
* REDIS_PORT=указать порт
* REDIS_HOST=указать хост
* QUIZ_DIR = название папки с txt вопросами
* QUIZ_DICT = json с готовыми вопросами с ответами
- воспользуйтесь командой 
```python
   cd functions
   python work_with_questions.py
```
для создания json с вопросами(ответами)
* PEER_ID = рандомные 6 чисел

4. В docker-compose заполните 
```      
      - REDIS_PASSWORD=${REDIS_PASSWORD}
      - REDIS_PORT=${REDIS_PORT}
```
      
* Собрать образ redis выполнив ```docker-compose up -d```


5. Для запуска программы:
```python tg_bot/tg_bot.py```
```python vk_bot/vk_bot.py```

