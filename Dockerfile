FROM tiangolo/uwsgi-nginx:python3.6
COPY ./uwsgi.ini /etc/uwsgi/uwsgi.ini
COPY ./nginx.conf /etc/nginx/conf.d/nginx.conf
ADD pip.txt .
RUN pip install -r pip.txt
