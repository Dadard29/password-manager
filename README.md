# Password manager

## Service

The service is a HTTP server, and can be accessed through several REST endpoints.

It allows you to access your secrets, stored on the remote server.

The documentation related to HTTP requests and to the API is available here:
`url here`

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
- `MASTER_KEY`: the key to use for database encryption. `TODO`
- `HTTP_HOST`: the host to listen on
- `HTTP_PORT`: the port to listen on
- `DEBUG`: tells if the service run in DEBUG mode (insecure)

Run the service using python:
```shell script
python service/main.py
```

TODO


### Session

The password manager is not multi-user. Only one user is supposed to access the service.

To decrypt the database and make the secrets available, you must provide the master key you specified in the environment.

### Data access

Now that you have you `token` ready, you can access your secrets.

TODO

### Session closing

If you do not use your `token` for more than the specified time, the session will be automatically closed, and the
database unloaded. All the changes you've done to your secrets are saved and written to the disk. You'll need to create
a new session to access your secrets.

If you want to check if your session is still valid, you can use the following request:
```http request
get request
```

If you want to close the session manually, you can use the following request:
```http request
delete request
```

## CLI

stuff

