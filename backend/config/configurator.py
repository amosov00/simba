from os import path

from sitri.providers.contrib.system import SystemConfigProvider

APP_ENV_PREFIX = "simba"
BASE_DIR = path.dirname(path.dirname(path.abspath(__file__)))

configurator = SystemConfigProvider(prefix=APP_ENV_PREFIX)

ENV = configurator.get("env")

IS_LOCAL = ENV == "local"
IS_PRODUCTION = ENV == "production"

local_mode_data_filename = None

if IS_LOCAL:
    local_mode_data_filename = configurator.get("local_mode_data_filename")
