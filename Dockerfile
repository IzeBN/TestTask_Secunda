FROM python:3.13.9

WORKDIR /backend

COPY requirments.txt .
RUN pip install --no-cache-dir -r requirments.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
