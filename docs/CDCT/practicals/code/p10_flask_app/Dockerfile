# p10_flask_app/Dockerfile
FROM python:3-alpine          # tiny base (~50 MB)
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
EXPOSE 80                     # document port
CMD ["python", "app.py"]