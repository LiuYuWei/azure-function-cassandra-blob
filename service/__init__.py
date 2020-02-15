import os
import sys

try:
    sys.path.append(os.environ['PROJECT_PATH'])
except:
    print('please add PROJECT_PATH to your environment')
    sys.exit(1)

import json
import logging
import azure.functions as func


from service.function_http_request import FunctionHttpRequest
from config.config_setting import ConfigSetting
from src.dao.cassandra_dao import CassandraDao
from src.dao.azure_blob_dao import AzureBlobService

def main(req: func.HttpRequest) -> func.HttpResponse:
    url_text = "None"
    config_setting = ConfigSetting()
    log = config_setting.set_logger("[ azure_function ]", os.path.join("tmp/", "logs"))
    log.info('Python HTTP trigger function processed a request.')

    function_http_request = FunctionHttpRequest(req)
    query_text = function_http_request.get_request_value('query_text')
    blob_store = function_http_request.get_request_value('blob_store')

    cassandra_dao = CassandraDao()
    cassandra_dao.connection_setting()
    
    df = cassandra_dao.get_query_data(query_text)
    
    log.info(blob_store)
    if blob_store == "True":
        log.info("存到azure blob中")
        output_csv_file = df.to_csv(index_label="idx", encoding = "utf-8")
        azure_blob_service = AzureBlobService()
        azure_blob_service.connection_setting()
        azure_blob_service.create_file_on_blob(output_csv_file)
        url_text = azure_blob_service.url_download_generate()
    df_json = df.to_json(orient='records',default_handler=str)

            
    json_text = json.dumps({"url":url_text, "data":df_json})
    if query_text:
        return func.HttpResponse(json_text)
    else:
        return func.HttpResponse(
             "Please pass a name on the query string or in the request body",
             status_code=400
        )
