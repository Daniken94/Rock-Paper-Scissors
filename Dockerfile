FROM ubuntu

RUN apt update
RUN apt install python3-pip -y
RUN pip3 install Flask==2.1.2
RUN pip3 install flask_sqlalchemy==2.5.1
RUN pip3 install pytz==2022.1

WORKDIR /app

COPY . .

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]