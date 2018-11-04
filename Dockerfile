FROM python:3.6
ENV PYTHONUNBUFFERED 1

RUN mkdir /database
RUN mkdir /database/nfl
RUN mkdir /database/nfl/data

WORKDIR /database/nfl/data
COPY init.sql /database/nfl/data


RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/

#RUN pip install --upgrade pip
RUN easy_install --upgrade pip
RUN pip install -r requirements.txt
RUN python -m pip install discord.py==0.16.12
ADD . /code/

# RUN apt-get update \
#     && apt-get install -y --no-install-recommends \
#         mysql-client \
#     && rm -rf /var/lib/apt/lists/*

#WORKDIR /usr/src/app
#COPY requirements.txt ./
# RUN pip install --upgrade pip

# RUN pip install Django
#RUN pip install -r requirements.txt

#COPY . .

#EXPOSE 8000

#RUN python manage.py runserver 
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
