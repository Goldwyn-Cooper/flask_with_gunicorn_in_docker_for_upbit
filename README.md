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

## Reference
### Flask & Gunicorn
* [flask with gunicorn](https://m.blog.naver.com/pareko/221918441176)
* [request.get_json()](https://m.blog.naver.com/sosow0212/222711187363)
* [How to return the status code in Flask](https://www.educative.io/answers/how-to-return-the-status-code-in-flask)