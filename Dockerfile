FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY analyzer.py .

RUN python analyzer.py --out /app/output/report.html

CMD ["python", "analyzer.py", "--out", "/app/output/report.html"]
