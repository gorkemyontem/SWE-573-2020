# Pull base image
FROM python:3.8

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install dependencies
COPY Pipfile Pipfile.lock /code/
RUN pip install pipenv && pipenv install --system --deploy

RUN pip3 install nltk
RUN [ "python", "-c", "import nltk; nltk.download('all')" ]
# # ENTRYPOINT python

# TODO python manage.py qcluster &          -- https://github.com/Koed00/django-q/issues/487



# Copy project
COPY . /code/
