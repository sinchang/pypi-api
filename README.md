# PyPi API

## Find a package

https://pypi-api.herokuapp.com/package/{package}

Example:

https://pypi-api.herokuapp.com/package/gunicorn

Response:

```
{
  "author": "Benoit Chesneau",
  "desc": "WSGI HTTP Server for UNIX",
  "homepage": "http://gunicorn.org",
  "license": "MIT License",
  "maintainers": [
    {
    "avatar": "https://secure.gravatar.com/avatar/d4f2d9a06f6ebab0f187e713696b4562?size=50",
    "name": "benoitc",
    "profile_url": "https://pypi.org//user/benoitc/"
    }
  ],
  "name": "gunicorn",
  "release_history": [
    {
    "date": "2017-03-21T03:00:49",
    "version": "19.7.1"
    }
  ],
  "status": 1
}
```

## Search packages

https://pypi-api.herokuapp.com/search?q={package}&page={page}

Example:

https://pypi-api.herokuapp.com/search?q=requests&page=1

Response:

```
{
  "projects": [
    {
      "desc": "Python HTTP for Humans.", 
      "latest_version": "2.18.4", 
      "name": "requests", 
      "url": "https://pypi.org/project/requests/"
    }
  ], 
  "status": 1
}
```

## License

 Licensed under the MIT license.