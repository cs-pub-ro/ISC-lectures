FROM debian:13

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential bash git curl ca-certificates \
    fontconfig fonts-liberation fonts-noto-cjk \
	libglib2.0-0 libnss3 libnspr4 libgbm1 libasound2 \
	libatk1.0-0 libatk-bridge2.0-0 libatspi2.0-0 libdbus-1-3 \
	libx11-6 libxcomposite1 libxdamage1 libxext6 libxfixes3 libxrandr2 \
	libxcb1 libxkbcommon0 potrace

RUN curl -fsSL "https://deb.nodesource.com/setup_lts.x" | bash -e - \
	&& apt-get update && apt-get install -y nodejs \
	&& npm -v

RUN npx playwright install-deps chromium

