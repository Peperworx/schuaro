FROM python:3.9

WORKDIR /app
COPY . /app

# Get poetry
RUN pip install poetry==1.1.6

WORKDIR /code

# Cache poetry files
COPY poetry.lock pyproject.toml /code/

# Disable poetry venvs
RUN python -m poetry config virtualenvs.create false


# Install
RUN python -m poetry install $(test "$SCHUARO_PROD" == production && echo "--no-dev")

# Copy code
COPY . /code

# Expose required ports
EXPOSE 80
EXPOSE 443
EXPOSE 4433/udp
EXPOSE 4433/tcp

# Run
CMD ["python","-m","schuaro"]