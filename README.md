# Tornado chat

## Requirements

BackEnd:
* Database - [MongoDB](http://www.mongodb.org/)
* WebServer/WebFramework - [Tornado](http://www.tornadoweb.org/)
* ODM - [Mongoengine](http://mongoengine.org/)

FrontEnd:
* [AngularJS](http://angularjs.org/) (use ajax.googleapis.com)
* [Twitter Bootstrap](http://getbootstrap.com/) (use netdna.bootstrapcdn.com)
* [JQuery](http://jquery.com/) (use ajax.googleapis.com) (bootstrap requirement)

## Instalation

    $ sudo apt-get install mongodb    #for Debian-based systems (or brew install for Mac)
    $ mkdir tornado_chat
    $ cd tornado_chat
    $ git clone https://github.com/SergeyTsaplin/tornado_chat.git
    $ pip install -r requirements.txt

After it you can to setup your local settings in *settings.py* file. And start
your application. Don't forget about mongo: before starting the app you have to
start mongo:


## Run application

Start MongoDB:

    $ mongod

Start application:

    $ cd /path/to/application
    $ python app.py

Open browser and go to http://localhost:5000
