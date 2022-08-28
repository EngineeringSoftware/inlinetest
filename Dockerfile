# docker build -t inlinetests .
# docker run -it inlinetests /bin/bash

# Pull base image
FROM texlive/texlive:latest-full

# Install sofware properties common
RUN apt-get update && \
    apt-get install -y software-properties-common
RUN rm /bin/sh && ln -s /bin/bash /bin/sh
RUN apt-get update && \
    apt-get -qq -y install apt-utils curl wget unzip zip gcc mono-mcs sudo emacs vim git build-essential

# Install miniconda
ENV CONDA_DIR /opt/conda
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
     /bin/bash ~/miniconda.sh -b -p /opt/conda
# Put conda in path so we can use conda activate
ENV PATH=$CONDA_DIR/bin:$PATH

# Add new user
RUN useradd -ms /bin/bash -c "Inlinetests User" inlinetests && echo "inlinetests:inlinetests" | chpasswd && adduser inlinetests sudo
USER inlinetests
WORKDIR /home/inlinetests/

# Install sdkman
RUN curl -s "https://get.sdkman.io" | bash && source "$HOME/.sdkman/bin/sdkman-init.sh"

# Set up working environment
COPY --chown=inlinetests:inlinetests . /home/inlinetests/

# init conda
RUN conda init bash && source ~/.bashrc

# Install python inline-dev
RUN cd "/home/inlinetests/python" && /bin/bash -c "bash prepare-conda-env.sh"
# Install python inline-research
RUN cd "/home/inlinetests/research" && /bin/bash -c "bash prepare-conda-env.sh"
# Install Java 8
RUN cd "/home/inlinetests/java" && /bin/bash -c "bash install.sh"