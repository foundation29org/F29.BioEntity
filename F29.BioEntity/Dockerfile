FROM python:3.7

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY . /app

EXPOSE 8080

WORKDIR /app

# Check included files
#RUN ls
#RUN ls _cache
#RUN ls _files

ENTRYPOINT ["python", "app.py"]
