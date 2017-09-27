FROM python:3.6.2
ENV PYTHONBUFFERED 1
ADD pip.txt .
RUN pip install -r pip.txt
