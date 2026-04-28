FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY analyzer.py .

RUN mkdir -p /app/output

RUN python analyzer.py --out /app/output/report.html

EXPOSE 9090

CMD ["python", "-m", "http.server", "9090", "--directory", "/app/output"]
