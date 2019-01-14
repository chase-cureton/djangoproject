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
RUN pip3 install djangorestframework
RUN python -m pip install discord.py==0.16.12

RUN rm /bin/sh && ln -s /bin/bash /bin/sh

RUN apt-get update \
    && apt-get install -y curl \
    && apt-get -y autoclean

#nvm environment variables
ENV NVM_DIR /usr/local/nvm
ENV NODE_VERSION 4.4.7

RUN curl --silent -o- https://raw.githubusercontent.com/creationix/nvm/v0.31.2/install.sh | bash

RUN source ${NVM_DIR}/nvm.sh \
    && nvm install ${NODE_VERSION} \
    && nvm alias default ${NODE_VERSION} \
    && nvm use default

ENV NODE_PATH = $NVM_DIR/v${NODE_VERSION}/lib/node_modules
ENV PATH $NVM_DIR/versions/node/v${NODE_VERSION}/bin:${PATH}

#RUN npm install
RUN npm install -g bower
#RUN bower install
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
