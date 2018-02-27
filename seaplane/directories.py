from seaplane.configuration.config import get_value
from seaplane.constants import PROJECT_DIR


class Directories:
    @property
    def DEVELOPMENT_DIR(self) -> str:
        return PROJECT_DIR + '/' + get_value('development_directory')

    @property
    def CHARTS_DIR(self) -> str:
        return self.DEVELOPMENT_DIR + '/' + get_value('charts_directory')

    @property
    def DOCKER_DIR(self) -> str:
        return self.DEVELOPMENT_DIR + '/' + get_value('docker_directory')

    def get_chart(self, chart) -> str:
        return self.CHARTS_DIR + '/' + chart
