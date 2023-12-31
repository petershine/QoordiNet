FROM python:3.12-slim
LABEL org.opencontainers.image.authors="petershine@fxceed.com"


WORKDIR /_python
RUN mkdir -p ./_mounted

# [_shared]: make sure to use actual folder, that was temporarily copied by the "redeploy.sh"
COPY ./mainApp/_temp_shared ./mainApp/_shared
RUN pip install --no-cache-dir --upgrade -r ./mainApp/_shared/requirements.txt

# [app_requirments.txt]
COPY ./mainApp/app_requirements.txt ./mainApp/
RUN pip install --no-cache-dir --upgrade -r ./mainApp/app_requirements.txt

# [mainApp]
COPY ./mainApp/*.py ./mainApp/
COPY ./mainApp/templates ./mainApp/templates
COPY ./mainApp/static ./mainApp/static


CMD ["python", "-m", "mainApp"]
