FROM ubuntu:21.04
RUN apt-get update -y && apt-get upgrade -y

# installing system tools
RUN apt-get install wget curl libmediainfo-dev -y

# install Python
RUN apt-get install build-essential -y
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get install libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev -y
RUN wget https://www.python.org/ftp/python/3.8.8/Python-3.8.8.tgz && tar xzf Python-3.8.8.tgz
WORKDIR /Python-3.8.8
RUN ./configure --with-openssl=/usr
RUN make altinstall
ENV PATH=$PATH:/Python-3.8.8
WORKDIR /
RUN rm Python-3.8.8.tgz

# installing Poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
ENV PATH=$PATH:/root/.poetry/bin
RUN poetry config virtualenvs.create false

# installing Metron Conduit SW requirements
RUN apt-get install ffmpeg=7:4.3.2-0+deb11u1ubuntu1 -y

# copying Metron Conduit source codes
RUN ls
ARG METRON_DIR=/metron
ARG METRON_SHARED_DIR=$METRON_DIR/shared
ARG METRON_CONDUIT_DIR=$METRON_DIR/metron_conduit
ADD shared $METRON_SHARED_DIR
ADD metron_conduit $METRON_CONDUIT_DIR
ADD poetry.lock .
ADD pyproject.toml .

# installing Metron Conduit
RUN cd $METRON_DIR && poetry install --no-dev
ENV PYTHONPATH=$METRON_DIR:
WORKDIR $METRON_CONDUIT_DIR
# download sample video which can be used as a demo showcase
RUN wget --no-check-certificate 'https://drive.google.com/uc?export=download&id=1upGnK5CVB3wbMNDCloPPDYrAnvjGKiYW' \
    -O sample_video.mp4