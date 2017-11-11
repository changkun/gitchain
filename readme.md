# Gitchain

GitHub repository meets crptocurrencies.

## Setup

**Fill your username and password of GitHub first** in [config/config.ini](config/config.ini), then:

```bash
# install environment
$ virtualenv -p python3 .env
$ source .env/bin/activate
$ pip install -r req.txt

# fetch repo data you want
$ python utils/creeper.py
```

## License

MIT &copy; Contributors