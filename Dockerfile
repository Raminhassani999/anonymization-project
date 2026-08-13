FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN python -m spacy download en_core_web_sm
RUN python -m spacy download it_core_news_sm

COPY . .

ENV PYTHONPATH=/app/src

RUN mkdir -p /app/output

CMD ["python", "-m", "main", "--detector", "spacy"]