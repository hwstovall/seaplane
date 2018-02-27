from colorama import Fore

from seaplane.utils.which import which

required_packages = [
    {
        'name': 'VirtualBox',
        'command': 'virtualbox',
        'install_link': 'https://www.virtualbox.org/wiki/Downloads'
    },
    {
        'name': 'Minikube',
        'command': 'minikube',
        'install_link': 'https://kubernetes.io/docs/tasks/tools/install-minikube/'
    },
    {
        'name': 'Docker',
        'command': 'docker',
        'install_link': 'https://docs.docker.com/install/#supported-platforms'
    },
    {
        'name': 'Helm',
        'command': 'helm',
        'install_link': 'https://github.com/kubernetes/helm/releases'
    },
]

recommended_packages = [
    {
        'name': 'Stern',
        'command': 'stern',
        'install_link': 'https://github.com/wercker/stern/releases'
    },
]


def check_requirements(recommended: bool) -> bool:
    packages = required_packages + recommended_packages if recommended else required_packages

    print('Checking for required packages...\n')
    header = 'Requirements'.ljust(30) + 'Installed'
    print(header)
    print('-' * len(header))

    footer = ''

    all_installed = True
    for package in packages:
        installed = which(package['command'])

        status = Fore.GREEN + '✓' if installed else Fore.RED + 'X'
        print(package['name'].ljust(34) + status)

        if not installed:
            all_installed = False

            footer += 'Install {name} here: {install_link}\n'.format(
                name=package['name'],
                install_link=package['install_link'])

    print('')

    if footer == '':
        footer = 'All requirements are installed! You\'re good to go.'
    else:
        footer = Fore.RED + 'Some requirements need to be installed first:\n' + Fore.RESET + footer

    print(footer)

    return all_installed
