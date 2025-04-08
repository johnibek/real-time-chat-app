ARG PYTHON_VERSION=3.12.3
FROM python:${PYTHON_VERSION}-slim as base


RUN mkdir /app
WORKDIR /app

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser


COPY requirements.txt /app/

RUN pip install -r requirements.txt

# Switch to the non-privileged user to run the application.
USER appuser

# Copy the source code into the container.
COPY . /app/

# Expose the port that the application listens on.
EXPOSE 8000

# Run the application.
CMD [ "daphne", "-b", "0.0.0.0", "-p", "8000", "core.asgi:application" ]
