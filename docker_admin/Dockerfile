FROM python:3.11

ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "${PYTHONPATH}:/"

WORKDIR /code/

RUN pip install uvicorn==0.21.0 django==4.1.7 python-dotenv==1.0.0 psycopg2-binary pillow==9.4.0 dj-database-url==2.0.0 whitenoise==6.5.0 django-jazzmin==2.6.0 django_select2==8.1.2

COPY . .
RUN chmod +x /code/entrypoint.sh

ENTRYPOINT ["sh", "entrypoint.sh"]

CMD ["make", "start"]