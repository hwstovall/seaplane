import os

from seaplane.configuration.config import get_value
from seaplane.constants import SEAPLANE_DIR, PROJECT_DIR
from seaplane.directories import Directories
from seaplane.utils.recursive_copy import recursive_copy

directories = Directories()


def ensure_directories():
    required_directories = [
        directories.DEVELOPMENT_DIR,
        directories.DOCKER_DIR,
        directories.CHARTS_DIR,
        directories.CHARTS_DIR + '/' + get_value('development_chart'),
    ]

    for directory in required_directories:
        if not os.path.exists(directory):
            os.makedirs(directory)


def ensure_example_files():
    recursive_copy(SEAPLANE_DIR + '/example/charts/demo', directories.get_chart(get_value('development_chart')))

    os.makedirs(directories.get_chart(get_value('development_chart')) + '/templates', exist_ok=True)
    recursive_copy(SEAPLANE_DIR + '/example/charts/demo/templates',
                   directories.get_chart(get_value('development_chart')) + '/templates')

    os.makedirs(directories.DOCKER_DIR + '/seaplane-example', exist_ok=True)
    recursive_copy(SEAPLANE_DIR + '/example/docker/seaplane-example', directories.DOCKER_DIR + '/seaplane-example')

    recursive_copy(SEAPLANE_DIR + '/example', PROJECT_DIR)
