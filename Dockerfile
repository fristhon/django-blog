FROM python:3.9.13

COPY requirements.txt requirements.txt
#TODO maybe not installing and running as root?
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /home/pyblog
COPY . .

EXPOSE 8000

RUN python pyblog/manage.py migrate
RUN python pyblog/manage.py initsuperuser
ENTRYPOINT ["python", "pyblog/manage.py"]
CMD ["runserver", "0.0.0.0:8000"]