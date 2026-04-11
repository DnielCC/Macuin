FROM python:3.11-slim

ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
ENV PYTHONUTF8=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# <-- Agrega el --reload al final
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]