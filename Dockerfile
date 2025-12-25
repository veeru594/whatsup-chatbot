FROM python:3.11-slim

WORKDIR /app
COPY . /app

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Optional: If using playwright for JS-heavy sites
# RUN playwright install
# RUN playwright install-deps

ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["uvicorn", "bot.webhook:app", "--host", "0.0.0.0", "--port", "8000"]
