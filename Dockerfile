FROM ubuntu:latest

WORKDIR /code

RUN apt update -y && \
    apt install wget -y && \
    wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
    sh Miniconda3-latest-Linux-x86_64.sh -b

ENV PATH /root/miniconda3/bin:$PATH

COPY ./article_env.yml /code

RUN conda env create -n article_env -f article_env.yml

CMD [ "/bin/bash" ]

RUN conda init bash && \
    echo "conda activate article_env" >> ~/.bashrc

ENV CONDA_DEFAULT_ENV article_env
ENV PATH /root/miniconda3/envs/article_env/bin/:$PATH