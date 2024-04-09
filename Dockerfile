FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /root/PycharmProjects/Cars_dealership

COPY ./requirements.txt /root/PycharmProjects/Cars_dealership/requirements.txt
RUN pip install -r /root/PycharmProjects/Cars_dealership/requirements.txt

COPY . /root/PycharmProjects/Cars_dealership

EXPOSE 8000

CMD python manage.py migrate && python manage.py runserver 0.0.0.0:8000