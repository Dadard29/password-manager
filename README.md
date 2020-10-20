# Password manager

## Service

The service is a HTTP server, and can be accessed through several REST endpoints.

It allows you to access your secrets, stored on the remote server.

### Session creation

The password manager is not multi-user. Only one user is supposed to access the service.

To be able to access your secrets, you need to open a session:
```http request
post request
```

The bearer token is the key, encoded in base64, to be used for the database encryption/decryption.

The response is expected to look like this: 
```http request
post response
```

The `token` field is the token to be used in the `Authorization` header, in all your next requests to the service.

The session is now opened, and the database loaded into memory. 

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

