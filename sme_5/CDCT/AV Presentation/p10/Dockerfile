FROM python:3-alpine
LABEL maintainer="CDCT Lab"
WORKDIR /usr/share/app
COPY p10_site/ ./p10_site/
EXPOSE 80
CMD ["python", "-m", "http.server", "80", "--directory", "p10_site"]