# UPBIT Flask

```bash
# IP 확인
$ curl ifconfig.me
```

```bash
# 세팅
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install --upgrade pip
# pip install pyupbit flask gunicorn -q
# pip freeze > requirements.txt
$ pip install -r requirements.txt
# flask run 
# gunicorn app:app
```