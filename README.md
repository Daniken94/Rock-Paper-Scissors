# Rock-Paper-Scissors
Simple web game in Rock-Paper-Scissors. Created in Flask

## Instalation:

Run the following command in your terminal:

Clone repository using SSH key:

```
git clone git@github.com:Daniken94/Rock-Paper-Scissors.git
```
or download 'zip'.

## Requirements:

Python is required !!!


You can install all app from requirements.txt by using command:

```
pip install -r requirements.txt
```

## Docker and Docker-compose:

Run the following command in your terminal:

```
docker-compose build
```

and

```
docker-compose up
```

In order to terminate the use and shut down the server it is necessary to run command in your terminal:

```
crtl + c
```

## Docker and Docker-compose error:

while problem with: 

```
"Got permission denied while trying to connect to the Docker daemon socket at unix:///var/run/docker.sock: Get http://%2Fvar%2Frun%2Fdocker.sock/v1.24/images/json: dial unix /var/run/docker.sock: connect: permission denied"
```

run command:

```
sudo chmod 666 /var/run/docker.sock
```