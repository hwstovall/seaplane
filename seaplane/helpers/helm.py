from subprocess import run, call
from typing import Optional

from seaplane.configuration.config import get_value
from seaplane.constants import PROJECT_DIR
from seaplane.utils.console import check_output_str
from seaplane.utils.logger import info_log


class Helm:
    def init(self):
        search = 'kubectl -n kube-system get deployments -o name'
        if 'tiller-deploy' in check_output_str(search.split(' ')):
            info_log('Removing existing tiller deployment.')
            delete_tiller = 'kubectl -n kube-system delete deployment tiller-deploy'
            run(delete_tiller.split(' '))

        info_log('Re-running helm init (idempotent).')
        init = 'helm init --wait'
        run(init.split(' '))

        info_log('Waiting for Tiller to be ready.')
        wait_for_rollout = 'kubectl rollout status -w deployment/tiller-deploy --namespace=kube-system'
        run(wait_for_rollout.split(' '))

    def install(self, name: str, chart: str, namespace: str, values: Optional[dict] = None):
        command = 'helm --name {name} --namespace {namespace} {values} install {chart}'.format(
            name=name,
            namespace=namespace,
            chart=chart,
            values=self._get_values(values),
        )
        call(command, shell=True)

    def upgrade(self, name: str, chart: str, namespace: str, values: Optional[dict] = None) -> None:
        command = 'helm upgrade --install --namespace {namespace} {values} {name} {chart}'.format(
            name=name,
            namespace=namespace,
            chart=chart,
            values=self._get_values(values),
        )
        print(command)
        call(command, shell=True)

    def delete(self, name: str) -> None:
        command = 'helm delete {name} --purge'.format(name=name)
        run(command.split(' '))

    def status(self, name: str) -> None:
        command = 'helm status {name}'.format(name=name)
        run(command.split(' '))

    def _get_values(self, other_values: Optional[dict] = None) -> str:
        values = {
            'projectDir': PROJECT_DIR,
            'hostName': get_value('project_hostname')
        }

        if other_values:
            values.update(other_values)

        values_string = ''
        for name, value in values.items():
            values_string += '--set {name}="{value}" '.format(
                name=name,
                value=value,
            )

        return values_string
