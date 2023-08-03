FROM python:3.9.13

WORKDIR /user_service

COPY ../../user_service/ /user_service

COPY ../../configs/user_service /user_service/configs

RUN pip install --no-cache-dir --upgrade -r requirements_service.txt

EXPOSE 8000

CMD ["python", "app.py"]
