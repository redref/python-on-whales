FROM busybox as get_buildx

RUN wget -O /docker-buildx https://github.com/docker/buildx/releases/download/v0.4.2/buildx-v0.4.2.linux-amd64
RUN chmod a+x /docker-buildx

#-----------------------------------------------------------------------------
FROM busybox as get_compose

RUN wget -O /docker-compose https://github.com/docker/compose-cli/releases/download/v2.0.0-beta.6/docker-compose-linux-amd64
RUN chmod a+x /docker-compose


#-----------------------------------------------------------------------------
FROM python:3.7 as python_dependencies

RUN pip install pydantic requests tqdm

COPY tests/test-requirements.txt /tmp/
COPY requirements.txt /tmp/
RUN pip install -r /tmp/test-requirements.txt -r /tmp/requirements.txt


#-----------------------------------------------------------------------------
FROM python_dependencies as lint
WORKDIR /python-on-whales
COPY . .
RUN flake8
RUN isort --check ./
RUN black --check ./

#-----------------------------------------------------------------------------
FROM python_dependencies as tests_with_binaries
COPY --from=docker:20.10 /usr/local/bin/docker /usr/bin/
COPY --from=get_buildx /docker-buildx /root/.docker/cli-plugins/
COPY --from=get_compose /docker-compose /root/.docker/cli-plugins/

WORKDIR /python-on-whales
ENV HOME=/root

COPY . .

RUN pip install -e .


CMD pytest -v --durations=10 ./tests


#-----------------------------------------------------------------------------
FROM python_dependencies as tests_without_any_binary

COPY --from=get_buildx /docker-buildx /root/.docker/cli-plugins/

WORKDIR /python-on-whales
COPY . .

RUN pip install -e .

CMD pytest -v --durations=10 ./tests/python_on_whales/components/buildx
