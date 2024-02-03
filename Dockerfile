FROM nvidia/cuda:12.2.0-base-ubuntu22.04

RUN apt-get update && apt-get upgrade -y

# Add repository to install python
RUN apt-get install software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa

# Setup timezone info for python installation
ENV TZ=Europe
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get install -y python3.11 python3-pip python3.11-venv

# Set python3.11 as default one
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1
RUN update-alternatives --config python3

# Set work dir
WORKDIR ./
COPY ./requirements/req.txt ./requirements.txt
COPY ./src ./src
RUN chmod 777 ./src

# Manage packages
RUN pip3 install --upgrade pip
RUN python3 -m venv venv
RUN . venv/bin/activate
RUN pip3 install --upgrade --ignore-installed -r requirements.txt

# Apply alembic migrations
# RUN alembic revision --autogenerate -m last_changes
# RUN alembic upgrade head

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "49100", "--workers", "2"]