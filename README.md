# TestAssessAI
Web app for automatic open answers verification

## Start
```sh
python -m venv venv
source venv/bin/activate # On Windows .\venv\Scripts\activate
python TestAssessAI/manage.py makemigrations
python TestAssessAI/manage.py migrate
python TestAssessAI/manage.py runserver
```

## ToDo
- `[ ]` Добавить количество попыток у теста и привязать к ним ответы.
- `[ ]` Добавить таблицу с группами студентов.
- `[ ]` Сделать модель датабазы.
- `[ ]` https://aistudio.google.com/ при помощи сделать оптравление и возвращение ответа 
- `[ ]` Так же можно будет в ответы на тест загрузить фотографию теста и оно будет проверенно искуственным интелектом
- `[ ]` Логин студентов и учителей будет проходить через LPAD.
- `[x]` Добавить автоматический логин после регистрации.