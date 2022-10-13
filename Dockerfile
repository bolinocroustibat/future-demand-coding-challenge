# Deriving the 3.9 base image
FROM python:3.9.13-alpine

# Any working directory can be chosen, like '/' or '/home' etc.
WORKDIR /

# Copy the remote file at working directory in container
COPY /src ./
# Now the structure looks like this '/src/main.py'

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "./main.py", "run", "--crawler-name='lucernefestival'"]
