FROM 812206152185.dkr.ecr.us-west-2.amazonaws.com/latch-base:9a7d-main

RUN curl --proto '=https' --tlsv1.2 https://sh.rustup.rs -sSf | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"
COPY data/brunello.csv /root/brunello.csv
COPY data/brie.csv /root/brie.csv

RUN apt-get install -y curl
RUN curl https://sh.rustup.rs -sSf | bash -s -- -y
RUN cargo install guide-counter
RUN python3 -m pip install cutadapt


# STOP HERE:
# The following lines are needed to ensure your build environement works
# correctly with latch.
COPY wf /root/wf
RUN python3 -m pip install --upgrade latch
ARG tag
ENV FLYTE_INTERNAL_IMAGE $tag
WORKDIR /root
