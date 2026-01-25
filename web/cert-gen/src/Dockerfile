FROM python:3.11-slim-bullseye

WORKDIR /app

RUN apt-get update && apt-get install -y \
    wget \
    ca-certificates \
    dnsutils \
    e2fsprogs \
    fontconfig \
    libxrender1 \
    libxext6 \
    libfontconfig1 \
    xfonts-75dpi \
    xfonts-base      

RUN wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1-2/wkhtmltox_0.12.6.1-2.bullseye_amd64.deb \
    && apt-get install -y ./wkhtmltox_0.12.6.1-2.bullseye_amd64.deb

RUN pip install flask pdfkit supervisor 

RUN useradd -m user

RUN echo "CYBNETIOT{jujurrr_izinn_bingung_mau_bikin_soal_apaa}" > /flag.txt \
    && chmod 444 /flag.txt \
    && chown root:root /flag.txt\
    && chown -R user:user /app

COPY . .

USER user

EXPOSE 3333 7777

CMD ["supervisord", "-c", "supervisord.conf"]
