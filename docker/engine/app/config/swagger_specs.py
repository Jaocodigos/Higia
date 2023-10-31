from flasgger import Swagger
from flask import Flask
from engine.app.config.logs import prepare_logs
import yaml
import codecs
import os

log = prepare_logs(__name__)


# Using Safe Loader because the default loader is deprecated


class APIDocs(Swagger):

    def load_swagger(self, filename):
        try:
            log.debug(f"Loading file: {filename}")
            filename = os.path.join(
                self.app.root_path,
                filename
            )
            if filename.endswith(".yaml") or filename.endswith(".yml"):
                loader = lambda stream: yaml.load(stream, Loader=yaml.SafeLoader)
            else:
                log.error(f"File {filename} is not supported, please introduce a yaml file.")
                raise FileNotFoundError("Yaml file has not found, exiting.")
            with codecs.open(filename, 'r', 'utf-8') as f:
                return loader(f)
        except FileNotFoundError:
            exit()
        except Exception as e:
            log.error(f"An error occurred while loading yaml file: {e}")


def set_swagger_config(app: Flask):
    app.config['SWAGGER'] = dict(
        title='Higia',
        openapi='3.0.1',
        version='1.0.0'
    )
