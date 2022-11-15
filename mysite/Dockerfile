FROM python:3.11-rc-bullseye

#The following configuration tells django to
#to write to the terminal in real time. 
#In this situation the output will not be buffered anywhere. 

ENV PYHTONUNBUFFERED 1

#The following configuration is used to
#create a new folder in your container.
#The folder will be the project's root folder 
#inside the container. 
#The folder will be used as the work directory
#for the subsequent commands. 

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

RUN python3 manage.py makemigrations mysite
RUN python3 manage.py migrate

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
