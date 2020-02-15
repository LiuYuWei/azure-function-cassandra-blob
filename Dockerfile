# To enable ssh & remote debugging on app service change the base image to the one below
# FROM mcr.microsoft.com/azure-functions/python:2.0-python3.6-appservice
FROM mcr.microsoft.com/azure-functions/python:2.0-python3.6

ENV AzureWebJobsScriptRoot=/home/site/wwwroot 
ENV AzureFunctionsJobHost__Logging__Console__IsEnabled=true
ENV PROJECT_PATH=${AzureWebJobsScriptRoot}

RUN apt-get update \
    && apt-get install tzdata \
    && dpkg-reconfigure --frontend noninteractive tzdata \
    && apt-get install -y libyaml-cpp-dev \
    libyaml-dev \
    && apt-get clean \
    && apt-get autoclean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* 

COPY requirements.txt /
RUN pip3 --no-cache-dir install -r /requirements.txt

WORKDIR ${AzureWebJobsScriptRoot}

COPY . /home/site/wwwroot