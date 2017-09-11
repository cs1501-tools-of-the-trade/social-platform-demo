# Introduction

This is the demo project for CS 1501 - Tools of the Trade (Web). It tries to put together everything that we will cover in this class.

This repo will contain commits that contain digestible chucks of information - things we'll cover in class. At the end, it will be a very simple but fully-functioning Twitter sort of clone. This repo is based off of this [Twitter clone for Flask](https://github.com/pallets/flask/tree/master/examples/minitwit).

As such, you can easily see the Tags and Releases for this repository. Each tag or release signifies a checkpoint introducing some new functionality that we had talked about in class.

This project consists of a Flask backend server and a relatively-raw frontend (just JavaScript and JQuery). We had a lot of back-and-forth to decide what to use and we chose this pair to maximize your potential to learn.


# Installation and environment setup

First, clone the repository to your computer:

```
git clone https://github.com/cs1501-tools-of-the-trade/social-platform-demo.git
```
Then navigate into the folder:
```
cd social-platform-demo
```

It's also a good idea to setup a Python `virtualenv` for yourself. This prevents conflicting dependencies with other projects/OS programs. If you don't already have it, we recommend installing it via `pip`:
```
pip install virtualenv
```
With it installed, you can actually create the environment within your project folder:
```
virtualenv env
```
Now you have an environment called `env`. To activate your new virtual environment (on MacOS/Unix), run:
```
source env/bin/activate
```
and on Windows run:
```
source env/Scripts/activate
```

You should now be in the virtual environment for Python and any packages you install via 'pip' will now only be installed into this directory.

To turn off the virtual environment, simply run
```
deactivate
```
Finally, you'll need to install all of the `pip` packages necessary to run this project. Using `pip freeze`, we exported all the packages we have a dependency on. This command installs them all at once:
```
pip install -r requirements.txt
```


# Starting the server

To start the Flask server, you will first need to configure a couple of environment variables. On MacOS, run:
```
export FLASK_APP=app.py
export FLASK_DEBUG=1
```
and on Windows run:
```
set FLASK_APP=app.py
set FLASK_DEBUG=1
```

Instead of having to call these commands every time, consider looking into the virtualenv `activate` file and putting the `EXPORT`/`set` call in there. That way, whenever you activate your environment, this will be done automatically. Let us know if you need help with this.

The `FLASK_DEBUG` variable tells Flask to enable debugging mode. For our purposes, this allows helpful messages for bugs and ability to hot deploy (reload code on refresh, instead of restarting the server). This is turned off in production deployments, for obvious reasons (making it an environment variable lets us do this easily).

To start the Flask development (debug) server, run the following:
```
flask run
```


# Credits
Created by [Nikhil Gupta](mailto:ng3br@virginia.edu) and [Srikanth Chelluri](mailto:sc5ba@virginia.edu).