import json
from subprocess import run, call

from seaplane.utils.console import check_output_str


class Kubectl:
    def delete(self, file: str, namespace: str):
        command = 'kubectl -n {namespace} delete -f {file}'.format(namespace=namespace, file=file)
        run(command.split(' '))

    def create(self, file: str, namespace: str):
        command = 'kubectl -n {namespace} create -f {file}'.format(namespace=namespace, file=file)
        run(command.split(' '))

    def apply(self, file: str, namespace: str):
        command = 'kubectl apply -f {file} --record'.format(namespace=namespace, file=file)
        run(command.split(' '))

    def exec(self, pod: str, command: str, namespace: str):
        command = 'kubectl -n {namespace} exec -it {pod} {command}'.format(
            namespace=namespace,
            pod=pod,
            command=command,
        )
        call(command, shell=True)

    def logs(self, pod: str, namespace: str):
        command = 'kubectl -n {namespace} logs {pod} -f'.format(
            namespace=namespace,
            pod=pod,
        )
        call(command, shell=True)

    def get_first_pod_name(self, label: str, value: str, namespace: str):
        command = 'kubectl -n {namespace} get po -l {label}={value} -o json'.format(
            namespace=namespace,
            label=label,
            value=value,
        )
        output = json.loads(check_output_str(command.split(' ')))

        return output['items'][0]['metadata']['name']
