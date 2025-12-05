FROM python:3.10.11
WORKDIR /usr/local/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./ ./
EXPOSE 8080

# Set up a separate user from root (https://docs.docker.com/build/building/best-practices/#user)
RUN useradd -m -u 1000 app

ENV HOME=/home/app

# If this line is ommitted, user "app" won't be able to create the ./model dir
RUN chown -R app:app /usr/local/app && \
    chown -R app:app /home/app

USER app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port","8080"]