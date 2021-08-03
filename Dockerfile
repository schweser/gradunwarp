FROM fsl603_freesurfer601

RUN apt-get update -y

RUN apt-get install -y build-essential python3 python3-pip python3-dev
RUN python3 -m pip install pip --upgrade


RUN apt-get install -y python-numpy
RUN apt-get install -y python-scipy


WORKDIR /code


RUN wget https://github.com/downloads/ksubramz/gradunwarp/nibabel-1.2.0.dev.tar.gz

RUN tar -xvzf nibabel-1.2.0.dev.tar.gz
WORKDIR /code/nibabel-1.2.0.dev
RUN python setup.py install

WORKDIR /code
COPY setup.py .

RUN mkdir /code/gradunwarp
WORKDIR /code/gradunwarp
COPY gradunwarp .

WORKDIR /code
RUN python setup.py install




