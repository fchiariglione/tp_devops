FROM python:alpine AS build
WORKDIR /app
COPY app/ .
COPY requirements.txt .
RUN pip install -r requirements.txt
EXPOSE 8000

FROM build AS test
COPY requirements-test.txt .
RUN pip install -r requirements-test.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]