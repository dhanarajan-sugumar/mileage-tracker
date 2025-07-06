# ── Build image ───────────────────────────────────────────────
FROM python:3.11-slim

ENV PATH="/root/.local/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

COPY mileage_app.py mileage_service.py ./ 
RUN mkdir -p data

EXPOSE 8501
CMD ["streamlit", "run", "mileage_app.py", "--server.port=8501", "--server.enableCORS=false"]
# ── Build image ───────────────────────────────────────────────
# docker build -t mileage-tracker .
# ── Run container ───────────────────────────────────────────────
# docker run -d -p 8501:8501 --name mileage-tracker mileage-tracker
# ── Access app ───────────────────────────────────────────────
# Open your browser and go to http://localhost:8501
# ── Stop container ───────────────────────────────────────────────
# docker stop mileage-tracker
# ── Remove container ───────────────────────────────────────────────
# docker rm mileage-tracker
# ── Remove image ───────────────────────────────────────────────
# docker rmi mileage-tracker
# ── Clean up unused images ───────────────────────────────────────────────
# docker image prune -f
# ── Clean up unused containers ───────────────────────────────────────────────
# docker container prune -f
# ── Clean up unused volumes ───────────────────────────────────────────────
# docker volume prune -f
# ── Clean up unused networks ───────────────────────────────────────────────
# docker network prune -f
# ── View logs ───────────────────────────────────────────────
# docker logs mileage-tracker