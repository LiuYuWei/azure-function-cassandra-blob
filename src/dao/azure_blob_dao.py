import os
import sys

try:
    sys.path.append(os.environ['PROJECT_PATH'])
except:
    print('please add PROJECT_PATH to your environment')
    sys.exit(1)

from time import time
from datetime import datetime, timedelta
from azure.storage.blob import BlockBlobService
from azure.storage.blob.models import BlobPermissions
from config.config_setting import ConfigSetting


class AzureBlobService:
    def __init__(self):
        config_setting = ConfigSetting()
        self.log = config_setting.set_logger("[ azure_function ]", os.path.join("tmp/", "logs"))
        self.config = config_setting.yaml_parser()
        self.blob_service_client = None
        self.file_name = None
    
    def connection_string_setting(self):
        connect_string = os.getenv('CONNECTION_STRING', default=self.config['azure']['blob']['connection_string'])
        return connect_string
    
    def account_name_setting(self):
        account_name = os.getenv('ACCOUNT_NAME', default=self.config['azure']['blob']['account_name'])
        return account_name

    def connection_setting(self):
        connect_string = self.connection_string_setting()
        self.blob_service_client = BlockBlobService(connection_string = connect_string)
        self.log.info("Successfully setting the connection.")

    def create_file_on_blob(self, df_csv_file):
        self.file_name = 'cassandra_query_{}.csv'.format(int(time()))
        self.blob_service_client.create_blob_from_text(
            self.config['azure']['blob']['container_name'], self.file_name, df_csv_file)
        self.log.info("Successfully create file on azure blob.")
    
    def url_download_generate(self):
        account_name = self.account_name_setting()
        container_name = self.config['azure']['blob']['container_name']
        blob_name = self.file_name

        self.log.info("Generate the url.")
        url = "https://{}.blob.core.windows.net/{}/{}".format(account_name,container_name,blob_name)
        token = self.blob_service_client.generate_blob_shared_access_signature(container_name, blob_name, permission=BlobPermissions.READ, expiry=datetime.utcnow() + timedelta(hours=1),)        
        self.log.info("Finish generate the url.")

        url_with_sas = "{}?{}".format(url, token)
        return url_with_sas
