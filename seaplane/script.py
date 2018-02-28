from subprocess import call

import click
from colorama import init

from seaplane.configuration.config import load_config, get_value
from seaplane.directories import Directories
from seaplane.helpers.docker import Docker
from seaplane.helpers.helm import Helm
from seaplane.helpers.kubectl import Kubectl
from seaplane.helpers.minikube import Minikube
from seaplane.utils.check_requirements import check_requirements
from seaplane.utils.console import check_output_str
from seaplane.utils.initialization import ensure_directories, ensure_example_files
from seaplane.utils.logger import info_log
from seaplane.utils.which import which

init(autoreset=True)

logo = '''
                      _                  
 ___  ___  __ _ _ __ | | __ _ _ __   ___ 
/ __|/ _ \/ _` | '_ \| |/ _` | '_ \ / _ \\
\__ \  __/ (_| | |_) | | (_| | | | |  __/
|___/\___|\__,_| .__/|_|\__,_|_| |_|\___|
               |_|                       
'''

load_config()

minikube = Minikube()
kubectl = Kubectl()
docker = Docker()
helm = Helm()

directories = Directories()


@click.group()
def seaplane():
    pass


@seaplane.command()
@click.option('--recommended', is_flag=True, default=False, help='Look for recommended packages.')
@click.option('--example', is_flag=True, default=False, help='Install the example app.')
def init(recommended, example):
    print(logo)

    if not check_requirements(recommended):
        return

    if minikube.is_running:
        print('\nIf you haven\'t added {hostname} to your hosts file, add the following line now.'.format(
            hostname=get_value('project_hostname')))
        print('{ip}     {hostname}\n'.format(
            ip=check_output_str(['minikube', 'ip']).strip(),
            hostname=get_value('project_hostname')))

    info_log('Ensuring your project has the directory structure and files Seaplane expects.')
    ensure_directories()

    if example:
        info_log('Copying example files.')
        ensure_example_files()


@seaplane.command()
def start():
    if not minikube.is_running:
        info_log('Starting Minikube...')
        minikube.start()
        helm.init()

    docker.build_all()

    info_log('Installing Helm charts...')
    helm.upgrade(name='nginx',
                 chart='stable/nginx-ingress',
                 namespace='kube-system',
                 values={
                     'controller.service.type': 'NodePort',
                     'controller.service.nodePorts.http': '80',
                 })
    helm.upgrade(name=get_value('project_name'),
                 chart=directories.get_chart(get_value('development_chart')),
                 namespace=get_value('namespace'))

    print('Your project, {project}, is now starting at http://{hostname}'.format(
        project=get_value('project_name'),
        hostname=get_value('project_hostname')))


@seaplane.command()
@click.option('--all', is_flag=True, default=False, help='Stop minikube cluster.')
def stop(all: bool):
    info_log('Deleting {project}...'.format(project=get_value('project_name')))
    helm.delete(get_value('project_name'))

    if all:
        info_log('Deleting nginx-ingress-controller...')
        helm.delete('nginx')

        minikube.stop()


@seaplane.command()
@click.argument('label')
@click.option('--namespace', default=get_value('namespace'), help='The namespace of the pod. Defaults to config value.')
@click.option('--executable', default='/bin/bash', help='The shell executable. Defaults to /bin/bash.')
def shell(label, namespace, executable):
    pod_name = kubectl.get_first_pod_name('seaplane-label', label, namespace)
    kubectl.exec(pod_name, executable, namespace)


@seaplane.command()
@click.argument('label')
@click.option('--namespace', default=get_value('namespace'), help='The namespace of the pod. Defaults to config value.')
def logs(label, namespace):
    if which('stern'):
        command = 'stern -n {namespace} -l seaplane-label={label}'.format(
            namespace=namespace,
            label=label,
        )
        call(command, shell=True)
    else:
        pod_name = kubectl.get_first_pod_name('seaplane-label', label, namespace)
        kubectl.logs(pod_name, namespace)


@seaplane.command()
def status():
    helm.status(get_value('project_name'))
