FROM tiangolo/uwsgi-nginx:python3.6
ADD . /diffseg
COPY ./uwsgi.ini /etc/uwsgi/uwsgi.ini
COPY ./nginx.conf /etc/nginx/conf.d/nginx.conf
ADD pip.txt .
RUN pip install -r pip.txt
RUN apt-get update; \
    apt-get install -y npm nodejs; \
    ln -s /usr/bin/nodejs /usr/bin/node; \
    npm install -g bower; \
    cd /diffseg/static && bower install --allow-root; \
    cd /diffseg && python manage.py collectstatic --no-input
