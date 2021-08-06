# See here for image contents: https://github.com/microsoft/vscode-dev-containers/tree/v0.187.0/containers/python-3/.devcontainer/base.Dockerfile

# [Choice] Python version: 3, 3.9, 3.8, 3.7, 3.6
ARG VARIANT="3.9"
FROM mcr.microsoft.com/vscode/devcontainers/python:0-${VARIANT}

# [Option] Install Node.js
ARG INSTALL_NODE="true"
ARG NODE_VERSION="lts/*"
RUN if [ "${INSTALL_NODE}" = "true" ]; then su vscode -c "umask 0002 && . /usr/local/share/nvm/nvm.sh && nvm install ${NODE_VERSION} 2>&1"; fi

# pip
RUN /usr/local/bin/python -m pip install --upgrade pip && \
    pip install lxml && \
    pip install cssselect && \
    pip install requests && \
    pip install beautifulsoup4 && \
    pip install requests-oauthlib &&

# forego
RUN wget https://bin.equinox.io/c/ekMN3bCZFUn/forego-stable-linux-amd64.deb && \
    apt-get -y install ./forego-stable-linux-amd64.deb

# [Optional] If your pip requirements rarely change, uncomment this section to add them to the image.
# COPY requirements.txt /tmp/pip-tmp/
# RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
#    && rm -rf /tmp/pip-tmp

# [Optional] Uncomment this section to install additional OS packages.
# RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
#     && apt-get -y install --no-install-recommends <your-package-list-here>

RUN apt-get update && \
    apt-get install -y mecab mecab-ipadic-utf8 libmecab-dev

# Please use the unOfficial mecab. For some reason the Official mecab only supports python2
# to use mecab-python3 requires the official mecab to be installed.
RUN pip install mecab-python3 && pip install unidic-lite
# [Optional] Uncomment this line to install global node packages.
# RUN su vscode -c "source /usr/local/share/nvm/nvm.sh && npm install -g <your-package-here>" 2>&1