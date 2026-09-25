FROM python:3.11-slim

WORKDIR /workspace

RUN useradd \
    --uid 10001 \
    --create-home \
    --shell /usr/sbin/nologin \
    releaseforge

COPY app/requirements.txt /workspace/app/requirements.txt

RUN pip install --no-cache-dir -r /workspace/app/requirements.txt

COPY app/ /workspace/app/

USER 10001

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]