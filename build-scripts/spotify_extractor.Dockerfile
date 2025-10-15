FROM python:3.12.6-slim
WORKDIR /src

COPY src/CloudRunJob/ ./src
RUN pip install --root-user-action=ignore --no-cache-dir --upgrade -r src/requirements.txt

CMD ["python", "src/main.py"]