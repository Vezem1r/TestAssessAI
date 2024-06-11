python -m venv venv
source venv/bin/activate # On Windows .\venv\Scripts\activate
python TestAssessAI/manage.py makemigrations
python TestAssessAI/manage.py migrate
python TestAssessAI/manage.py runserver