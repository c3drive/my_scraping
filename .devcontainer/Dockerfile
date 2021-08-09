# See here for image contents: https://github.com/microsoft/vscode-dev-containers/tree/v0.187.0/containers/python-3/.devcontainer/base.Dockerfile

# [Choice] Python version: 3, 3.9, 3.8, 3.7, 3.6
ARG VARIANT="3.9"
FROM mcr.microsoft.com/vscode/devcontainers/python:0-${VARIANT}

# [Option] Install Node.js
# trueにすると、/usr/local/share/nvm/nvm.shでエラーになる。
# [2021-08-07T12:41:55.094Z] Version 'lts' not found - try `nvm ls-remote` to browse available versions.
# [2021-08-07T12:41:55.458Z] The command '/bin/sh -c if [ "${NODE_VERSION}" != "none" ]; then su vscode -c "umask 0002 && . /usr/local/share/nvm/nvm.sh && nvm install ${NODE_VERSION} 2>&1"; fi' returned a non-zero code: 3
# nvm ls-remote`でnvmを更新することでnodeバージョンの指定が可能になり解消するが、今までできていたことが8/7になってできなくなったため不明。特に用途もないのでnoneにしておく。
ARG INSTALL_NODE="false"
ARG NODE_VERSION="lts/*"
RUN if [ "${INSTALL_NODE}" = "true" ]; then su vscode -c "umask 0002 && . /usr/local/share/nvm/nvm.sh && nvm install ${NODE_VERSION} 2>&1"; fi

# pip
RUN /usr/local/bin/python -m pip install --upgrade pip && \
    pip install lxml && \
    pip install cssselect && \
    pip install requests && \
    pip install beautifulsoup4 && \
    pip install requests-oauthlib && \
    pip install wikiextractor && \
    pip install pymongo && \
    pip install google-api-python-client & \
    pip install pandas && \
    pip install xlrd && \
    pip install openpyxl && \
    pip install matplotlib && \
    pip install japanize-matplotlib && \
    pip install pdfminer.six && \
    pip install selenium &&\
    pip install SPARQLWrapper && \
    pip install scrapy && \
    pip install readability && \
    pip install readability-lxml


# PhantomJS
# RUN wget https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2 && \
#     tar xvf phantomjs-2.1.1-linux-x86_64.tar.bz2 && \
#     cp phantomjs-2.1.1-linux-x86_64/bin/phantomjs /usr/local/bin/ && \

# Chrome(依存関係でdpkgエラーになる可能性があるので先に解消する)
RUN apt-get update && apt-get install -f
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt-get install -y ./google-chrome-stable_current_amd64.deb

# RUN apt-get install -y python3-selenium
RUN apt install unzip
RUN wget https://chromedriver.storage.googleapis.com/92.0.4515.107/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip && \
    sudo mv chromedriver /usr/local/bin/
# スクリーンショット時のキャプチャ日本語化
RUN apt-get install -y libfontconfig1 fonts-migmix

# forego
RUN wget https://bin.equinox.io/c/ekMN3bCZFUn/forego-stable-linux-amd64.deb && \
    apt-get -y install ./forego-stable-linux-amd64.deb

# MongDB
# RUN wget -qO - https://www.mongodb.org/static/pgp/server-5.0.asc | sudo apt-key add - && \
#     echo "deb http://repo.mongodb.org/apt/debian buster/mongodb-org/5.0 main" | sudo tee /etc/apt/sources.list.d/mongodb-org-5.0.list && \
#     apt-get update && \
#     apt-get install -y mongodb-org

# sqlite
RUN apt-get install -y sqlite3
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