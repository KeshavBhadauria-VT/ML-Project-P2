FROM python:3.9
# Install wait-for-it script
RUN mkdir /backend
WORKDIR /backend
COPY requirements.txt /backend/requirements.txt
RUN pip install --upgrade pip && \
    pip install -r requirements.txt
COPY . .

# Install black (assuming it's not already installed)
RUN pip install black

# For deploying
CMD ["flask", "--app", "app.py", "--debug", "run", "--host=0.0.0.0"]
