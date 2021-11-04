cd mysite/
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'pass')" | python manage.py shell
python manage.py loaddata startup_data.json
osascript -e 'tell app "Terminal" to do script "python -m smtpd -n -c DebuggingServer localhost:1025"'
python manage.py runserver

