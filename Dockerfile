FROM python:3.6.6-slim
ADD . /Demoapp
WORKDIR /Demoapp
RUN pip install -r requirements.txt
CMD python ./Demoapp/app.py

