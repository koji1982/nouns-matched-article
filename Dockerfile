FROM ubuntu:latest

WORKDIR /code

ENV PATH /opt/conda/bin:$PATH

RUN apt-get update -y && \
    apt-get install -y tzdata && \
    apt-get install -y wget apache2 apache2-dev && \
    wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
    sh Miniconda3-latest-Linux-x86_64.sh -b -p /opt/conda && \
    rm Miniconda3-latest-Linux-x86_64.sh && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY ./article_env.yml /code

RUN conda env create -n article_env -f article_env.yml

CMD [ "/bin/bash" ]

RUN conda init bash && \
    echo "conda activate article_env" >> ~/.bashrc && \
    find /opt/conda/ -follow -type f -name '*.a' -delete && \
    find /opt/conda/ -follow -type f -name '*.js.map' -delete && \
    /opt/conda/bin/conda clean -afy

ENV CONDA_DEFAULT_ENV article_env
ENV PATH /opt/conda/envs/article_env/bin/:$PATH