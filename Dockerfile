ARG PYTHON_VERSION=3.12-slim

FROM python:${PYTHON_VERSION} AS build

# Create venv
RUN python -m venv /app/venv
# Use virtualenv
ENV PATH="/app/venv/bin:$PATH"

# Copy and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ /app


FROM python:${PYTHON_VERSION} AS serve

ARG USERNAME=app
ARG USER_UID=1000
ARG USER_GID=$USER_UID
ARG APP_DIR="/app"

# Create group and user without homedir
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -M $USERNAME

COPY --from=build --chown=$USERNAME:$USERNAME $APP_DIR $APP_DIR

# Use virtualenv
ENV PATH="/app/venv/bin:$PATH"

WORKDIR $APP_DIR

USER $USERNAME

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
