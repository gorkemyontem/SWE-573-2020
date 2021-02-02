# SWE 573 - Software Development Practice
This repository has been created for SWE573 Software Development Practice course.

# Sentiment Analyser 
Sentiment Analyser is an open-source project for sentiment analysis. It extracts public information from Reddit API and visualizes the data. It is made for scientists by developers.
<br><br>
  ## Installation - Prerequisite

Clone the repo to your environment 
```bash
git clone https://github.com/gorkemyontem/SWE-573-2020.git
```

<br><br>
## Installation - Docker Compose
The instructions assume that you have already installed [Docker](https://docs.docker.com/installation/) and [Docker Compose](https://docs.docker.com/compose/install/). 

```bash
docker-compose up
```

<br><br>
## Installation - Docker

The instructions assume that you have already installed [Docker](https://docs.docker.com/installation/).

```bash
docker build -t sentiment-analyser .
```

<br><br>
## Installation - Pip
The instructions assume that you have already installed [pip](https://pip.pypa.io/en/stable/).


```bash
pip install pipenv
```

```bash
pip install nltk
```

```bash
pipenv install  
```

```bash
pipenv shell 
```

```bash
python manage.py runserver
```
<br><br>
## Creating Admin User
In order to use Django Admin Panel use the code below and set username and password.
```bash
python manage.py createsuperuser
```
<br><br>
## Migration

To generate migrations:
```bash
python manage.py makemigrations [APP_NAME]
```

To see the migrations:
```bash
python manage.py showmigrations [APP_NAME]
```
To run the migrations:

```bash
python manage.py migrate [APP_NAME]
```

<br><br>
## Scheduler - DjangoQ
This project crawl public API asynchronously. It's highly dependent on DjangoQ

To run the scheduler: 
```bash
python manage.py qcluster
```

To monitor the jobs: 
```bash
python manage.py qmonitor
```

To get general info about the jobs: 
```bash
python manage.py qinfo
```

<br><br>
# Test

Run all of the tests
```bash
python manage.py test
```

Run coverage.py to measuring code coverage
```bash
coverage run --omit='*/.virtualenvs/*' manage.py test
```

```bash
coverage report
```
OR for html output
```bash
coverage html
```
<br><br>
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
