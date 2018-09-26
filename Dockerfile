FROM python:3.6.6-slim
ADD . /Demoapp
WORKDIR /Demoapp
RUN pip3 install -r requirements.txt
CMD python ./run.py
