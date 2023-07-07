#!/bin/sh

echo "Start"

# pid=$(ps aux | grep '[d]jango' | awk '{print $2}')
# echo $(ps aux)
# kill -9 $(lsof -t -i:8000)
cd ..
git pull origin development
# cd crbrm/
python3 manage.py migrate
python3 manage.py makemigrations
# python3 manage.py runserver

echo "Done"