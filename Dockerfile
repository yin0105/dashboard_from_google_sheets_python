# FROM python:3.7.9
# COPY . /app
# WORKDIR /app
# RUN pip install -r requirements.txt
# ENTRYPOINT ["python"]
# RUN chmod 644 application.py
# CMD ["application.py"] -p 5000:5000

FROM python:3.7.9 
COPY . /app
WORKDIR /app
# RUN LANG="pt_BR.UTF-8"
# RUN export LC_ALL="pt_BR.UTF-8"
# RUN export LC_CTYPE="pt_BR.UTF-8"
RUN apt-get update && \
    apt-get install -y locales && \
    sed -i -e 's/# pt_BR.UTF-8 UTF-8/pt_BR.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales
ENV LANG pt_BR.UTF-8
ENV LC_ALL pt_BR.UTF-8

RUN pip install -r requirements.txt 
EXPOSE 5000 
RUN chmod 777 /app/static/chart
RUN chmod 777 /app/static/app-assets/images
ENTRYPOINT [ "python" ] 
CMD [ "application.py" ] 
# docker run -p 5002:5002 docktoflask

# FROM usgsastro/debian:8

# ENV PIP_CERT /etc/ssl/certs/ca-certificates.crt
# ENV REQUESTS_CA_BUNDLE /etc/ssl/certs/ca-certificates.crt

# RUN apt-get update && \
#     apt-get install -y \
#         libffi-dev \
#         libc-ares-dev \
#         python \
#         python-dev \
#         python-pip \
#     && rm -rf /var/cache/apt/* /var/lib/apt/lists/*

# RUN useradd -m appuser

# WORKDIR /home/appuser
# COPY . app
# RUN chown -R appuser:appuser app

# WORKDIR app
# USER appuser

# ENV PATH "/home/appuser/.local/bin:$PATH"
# RUN pip install --upgrade --user pip
# RUN pip install --user -U pip 'setuptools<45' && pip install --user -r requirements.txt

# EXPOSE 8000
# CMD gunicorn tiles:app -b :8000 --workers=2 -k gevent -t 45 --log-level=DEBUG
