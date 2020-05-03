FROM python:3.8-slim

RUN apt update && apt install -y curl \
  && curl -L https://get.helm.sh/helm-v3.2.0-linux-amd64.tar.gz \
    | tar -zx --strip-components=1 --directory=/usr/local/bin linux-amd64/helm

RUN pip install poetry
ENV POETRY_VIRTUALENVS_CREATE false

WORKDIR /usr/local/src
COPY pyproject.toml poetry.lock ./
RUN poetry install

COPY helm-template.py ./

ENTRYPOINT ["/usr/local/bin/python", "/usr/local/src/helm-template.py"]
# CMD ["python", "helm-template.py"]
