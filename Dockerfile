# docker build -t inlinetests .
# docker run -it inlinetests /bin/bash

# Pull base image
FROM texlive/texlive:latest-full

# Install sofware properties common
RUN apt-get update && \
    apt-get install -y software-properties-common
RUN rm /bin/sh && ln -s /bin/bash /bin/sh
RUN apt-get update && \
    apt-get -qq -y install apt-utils curl wget unzip zip gcc mono-mcs sudo emacs vim less git build-essential pkg-config libicu-dev

# Install miniconda
ENV CONDA_DIR /opt/conda
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
     /bin/bash ~/miniconda.sh -b -p /opt/conda
# Put conda in path so we can use conda activate
ENV PATH=$CONDA_DIR/bin:$PATH

# Add new user
RUN useradd -ms /bin/bash -c "Inlinetests User" itdocker && echo "itdocker:itdocker" | chpasswd && adduser itdocker sudo
USER itdocker
WORKDIR /home/itdocker/

# Install sdkman
RUN curl -s "https://get.sdkman.io" | bash && source "$HOME/.sdkman/bin/sdkman-init.sh"

# Set up working environment
RUN git clone https://github.com/pengyunie/inlinetest.git inlinetest

# init conda
RUN conda init bash && source ~/.bashrc

# Install python inline-dev
RUN cd "$HOME/inlinetest/python" && /bin/bash -c "bash prepare-conda-env.sh"
# Install python inline-research
RUN cd "$HOME/inlinetest/research" && /bin/bash -c "bash prepare-conda-env.sh"
# Install Java 8
RUN cd "$HOME/inlinetest/java" && /bin/bash -c "bash install.sh"

ENTRYPOINT /bin/bash