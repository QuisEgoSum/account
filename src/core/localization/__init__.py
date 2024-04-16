from qstd_core import localization
from src.core.config import config

localization.State.load(config.root_dir + '/resources/localization')
