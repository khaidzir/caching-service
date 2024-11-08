FROM python:3.11

WORKDIR /app

# Install Tini
ENV TINI_VERSION v0.19.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
RUN chmod +x /tini

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY app/ /app/app/

RUN rm requirements.txt

ENTRYPOINT [ "/tini", "--" ]
CMD ["fastapi", "run", "app/main.py", "--port", "80"]
