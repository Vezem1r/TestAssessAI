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