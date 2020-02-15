import os
import sys

try:
    sys.path.append(os.environ['PROJECT_PATH'])
except:
    print('please add PROJECT_PATH to your environment')
    sys.exit(1)

from config.config_setting import ConfigSetting
import azure.functions as func

class FunctionHttpRequest:
    def __init__(self, req):
        config_setting = ConfigSetting()
        self.log = config_setting.set_logger("[ azure_function ]", os.path.join("tmp/", "logs"))
        self.config = config_setting.yaml_parser()
        self.req = req

    def get_request_value(self, query_parameter_key_name):
        query_text = self.req.params.get(query_parameter_key_name)
        if not query_text:
            try:
                req_body = self.req.get_json()
            except ValueError as e:
                log.info("ValueError: {}".format(e))
            else:
                query_text = req_body.get(query_parameter_key_name)
        return query_text