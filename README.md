# Password manager

## Service

The service is a HTTP server, and can be accessed through several REST endpoints.

It allows you to access your secrets, stored on the remote server.

The documentation related to HTTP requests and to the API is available [here](https://documenter.getpostman.com/view/7424587/TVes6mXr).

### Setup

Clone this repo on the machine where you want to host the service. The machine must be reachable with HTTP. 
```shell script
git clone https://github.com/Dadard29/password-manager.git
```

Put an empty file on your machine at the location you want. This file will store the database encrypted. For example:
```shell script
touch db/default.db
```

Configure the following environment variables:
- `DB_PATH`: the location of the database file
- `MASTER_KEY`: the key to use for database encryption.
- `HTTP_HOST`: the host to listen on
- `HTTP_PORT`: the port to listen on
- `DEBUG`: tells if the service run in DEBUG mode (**insecure!!!**)

Run the service using python:
```shell script
python service/main.py
```

### Session

The password manager is not multi-user. Only one user is supposed to access the service.

To access the secrets stored, you need to create a session.
To proceed, submit the master key to the endpoint `session`.
When done, the service loads the database file content, decrypts it, and stores it into memory.
It also gives a temporary `token`, which allow to access the data.

### Data access

Now that you have you have a valid temporary `token`, you can access your secrets.
You can create, retrieve, update and delete secrets. A secret object looks like this:
```json
{
    "content": {
      "metas": {
        "username": "username1"
      },
      "value": "value1"
    },
    "created_at": "18 Nov. 2020 20:27",
    "type": "entry",
    "updated_at": "18 Nov. 2020 20:27"
  }
```
You can also create and create directories to organize your secrets.
You can also list the content of those directories.


### Session closing

After you are finished editing the database, you can close the session manually.
When done, the service will unload the decrypted content from memory.

If you don't close the session, it will be closed automatically after a certain amount of time of inactivity.
This timeout can be configured in the file `service/config/config.py` 

## CLI

You can access and manage your secrets through the CLI. The options are documented.
```shell script
python cli/main.py --help
``` 

With this CLI, you can get an interactive terminal.
You must fulfill the host where the service is hosted, with the scheme and the HTTP port.
You can also add the option `--debug` to get more information about the service interactions.
Enter your master key when prompted.
```shell script
python cli/main.py --host http://localhost:5000
master key: ******
session created
*connected*, type help or ? for a list of commands

[localhost] (/):
```

All commands are documented
```shell script
[localhost] (/): help

Documented commands (type help <topic>):
========================================
cd  get  help  ls  mkdir  quit  refresh  rm  rmdir  set
```

You can access all the service features with those commands.

## TL;DR

**INSECURE CONFIG, READ ALL THE DOCS FOR A SECURE USAGE**

- Installation
```shell script
git clone https://github.com/Dadard29/password-manager.git
python -m venv venv
source venv/bin/activate
pip install -r requirements
```

- Service setup
```shell script
touch db/default.db
export DB_PATH=db/default.db
export MASTER_KEY=*****
export HTTP_HOST=0.0.0.0
export HTTP_PORT=5000
export DEBUG=1
python service/main.py
```

- CLI run
```shell script
python main.py --debug --host http://localhost:5000
master key: *****
creating a new session...
session created
*connected*, type help or ? for a list of commands

[localhost] (/):
```


