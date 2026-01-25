FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    libarchive-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m ctf

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN sh -c 'FLAG_NAME="$(head /dev/urandom | tr -dc A-Za-z0-9 | head -c 16).txt" && \
    echo "CYBNETIOT{arch1ve_traversal_is_st1ll_aliv3}" > "/$FLAG_NAME" && \
    chown root:ctf "/$FLAG_NAME" && \
    chmod 440 "/$FLAG_NAME"'

RUN chown -R root:root /app && \
    chmod -R 555 /app

RUN mkdir -p /tmp/workspaces && \
    chown -R ctf:ctf /tmp/workspaces && \
    chmod 777 /tmp/workspaces

USER ctf

EXPOSE 5000

CMD ["python", "-B", "app.py"]