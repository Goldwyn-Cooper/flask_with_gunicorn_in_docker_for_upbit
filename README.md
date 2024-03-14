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
# pip install pyupbit flask gunicorn gevent -q
# pip freeze > requirements.txt
$ pip install -r requirements.txt
# flask run 
# gunicorn app:app -b 0.0.0.0:8000 -w 2 --timeout 10
# mkdir logs
# gunicorn app:app -b 0.0.0.0:8000 -w 2 -k gevent --timeout 10 --error-logfile logs/gunicorn.error.log --access-logfile logs/gunicorn.log --capture-output
$ gunicorn app:app --reload
```

```bash
# Docker
$ docker build -t upbit-flask .
$ docker run --name upbit-flask -d -p 80:80 -v ./logs:/usr/src/app/logs upbit-flask
```

## Reference
### Docker
* [[Docker] Dockerfile 개념 및 작성법](https://wooono.tistory.com/123)
* [Run our Flask app with gunicorn in Docker](https://rest-apis-flask.teclado.com/docs/deploy_to_render/docker_with_gunicorn/)
* [Flask + Gunicorn with Docker](https://velog.io/@windsekirun/Flask-Gunicorn-with-Docker)
### Flask & Gunicorn
* [Gunicorn : Settings](https://docs.gunicorn.org/en/stable/settings.html#settings)
* [flask with gunicorn](https://m.blog.naver.com/pareko/221918441176)
* [request.get_json()](https://m.blog.naver.com/sosow0212/222711187363)
* [How to return the status code in Flask](https://www.educative.io/answers/how-to-return-the-status-code-in-flask)