# coding=UTF-8
import os
import sys

try:
    sys.path.append(os.environ['PROJECT_PATH'])
except:
    print('please add PROJECT_PATH to your environment')
    sys.exit(1)

import pandas as pd
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

from config.config_setting import ConfigSetting

class CassandraDao:
    def __init__(self):
        config_setting = ConfigSetting()
        self.log = config_setting.set_logger("[ azure_function ]", os.path.join("tmp/", "logs"))
        self.config = config_setting.yaml_parser()
        self.session = None
    
    def connection_uri_variable_setting(self):
        """ Auth setting. """
        username = os.getenv('CASSANDRA_USER', default=self.config['cassandra']['username'])
        password = os.getenv('CASSANDRA_PASSWORD',default=self.config['cassandra']['password'])
        host = os.getenv('CASSANDRA_HOST', default=self.config['cassandra']['host'])
        port = os.getenv('CASSANDRA_PORT', default=self.config['cassandra']['port'])
        return username, password, host, port

    def connection_setting(self):
        """ Connection setting. """
        username, password, host, port = self.connection_uri_variable_setting()
        auth_provider = PlainTextAuthProvider(username=username, password=password)
        cluster = Cluster(host, port=port, protocol_version=self.config['cassandra']['protocol'],auth_provider=auth_provider)
        self.session = cluster.connect(wait_for_all_pools=self.config['cassandra']['wait_for_all_pools'])
    
    def keyspace_transfer(self, keyspace_name):
        """ Transfer keyspace. """
        self.session.execute('USE {}'.format(keyspace_name))
        log.info("Successfully transfer the keyspace to {}".format(keyspace_name))

    def get_query_data(self, query_text):
        """ Query data. """
        rows = self.session.execute(query_text)
        return pd.DataFrame(rows)
    