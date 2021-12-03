FROM python:latest
WORKDIR /usr/src/projet-i3-sneaker
COPY requirements.txt requirements.txt
RUN pip3 install --upgrade pip
RUN python3 -m pip install --upgrade https://storage.googleapis.com/tensorflow/mac/cpu/tensorflow-0.12.0-py3-none-any.whl
RUN pip3 install -r requirements.txt
COPY . .
WORKDIR /usr/src/projet-i3-sneaker/src
CMD ["python", "./run.py"]