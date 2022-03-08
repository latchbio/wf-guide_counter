FROM 812206152185.dkr.ecr.us-west-2.amazonaws.com/wf-base:fbe8-main

RUN curl --proto '=https' --tlsv1.2 https://sh.rustup.rs -sSf | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"
COPY data/brunello.csv /root/brunello.csv

RUN cargo install guide-counter

# STOP HERE:
# The following lines are needed to ensure your build environement works
# correctly with latch.
WORKDIR /root
COPY wf /root/wf
ARG tag
ENV FLYTE_INTERNAL_IMAGE $tag
ENV LATCH_AUTHENTICATION_ENDPOINT https://nucleus.latch.bio
RUN  sed -i 's/latch/wf/g' flytekit.config
RUN python3 -m pip install --upgrade latch
