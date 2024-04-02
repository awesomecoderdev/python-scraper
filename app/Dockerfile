# Dockerfile
FROM python:3.8

# Install entr
RUN apt-get update && apt-get install -y entr

WORKDIR /app

COPY requirements.txt requirements.txt
RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install -r requirements.txt

COPY . .


# Use entr to run app.py and monitor for changes
CMD ["sh", "-c", "ls /app/app.py | entr -rn python3 /app/app.py"]