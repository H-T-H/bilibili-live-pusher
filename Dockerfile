FROM python:3.9-alpine
WORKDIR /app
COPY ./ /app/
RUN pip install --no-cache-dir -r requirements.txt
CMD ["sh", "-c", "python main.py"]