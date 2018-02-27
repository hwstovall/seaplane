import re
from subprocess import run
from typing import Dict

from seaplane.configuration.config import get_value
from seaplane.utils.console import check_output_str


class Minikube:
    def start(self):
        command = 'minikube start -v 3 --extra-config=apiserver.ServiceNodePortRange={port_range}'.format(
            port_range=get_value('port_range')
        )
        run(command.split(' '))
        self.fix_linux_hostname()

    def stop(self):
        command = 'minikube stop'
        run(command.split(' '))

    def fix_linux_hostname(self):
        self.ssh('if [ -d /hosthome ]; then sudo ln -s /hosthome/* /home/ ; fi')

    @staticmethod
    def set_context():
        command = 'kubectl config use-context minikube'
        run(command.split(' '))

    @staticmethod
    def get_docker_env() -> Dict[str, str]:
        command = 'minikube docker-env'
        result = check_output_str(command.split(' ')).split('\n')

        docker_env = {}
        for line in result:
            match = re.search('export\s([A-Z_]+=\".+\")', line)

            if match:
                export = match.groups()[0]
                name, value = export.replace('\"', '').split('=')

                docker_env[name] = value

        return docker_env

    @staticmethod
    def ssh(command: str):
        run(['minikube', 'ssh', command])

    @property
    def is_running(self) -> bool:
        try:
            command = 'minikube status'
            status = check_output_str(command.split(' '))
            return 'minikube: Running' in status
        except:
            # If the above command fails, minikube is definitely not running.
            return False
