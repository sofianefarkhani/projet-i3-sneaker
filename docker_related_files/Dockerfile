FROM tensorflow/tensorflow
WORKDIR /usr/projet-i3-sneaker
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
WORKDIR /usr/projet-i3-sneaker/src
CMD ["python", "run.py"]