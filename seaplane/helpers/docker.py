import os
from subprocess import run
from typing import Dict, Optional

from seaplane.directories import Directories
from seaplane.helpers.minikube import Minikube
from seaplane.utils.logger import info_log

DockerEnv = Dict[str, str]

directories = Directories()


class Docker:
    def build(self, dockerfile: str, image_tag: str, env: Optional[DockerEnv] = None):
        env = env or Minikube.get_docker_env()

        command = 'docker build -t {image_tag} -f {dockerfile} .'.format(
            dockerfile=dockerfile,
            image_tag=image_tag,
        )

        print(env)
        run(command.split(' '), env=env)

    def build_simple(self, image: str, tag: Optional[str] = None):
        image_tag = image

        if tag:
            image_tag += ':{tag}'.format(tag=tag)

        dockerfile = '{docker_directory}/{image}/Dockerfile'.format(
            docker_directory=directories.DOCKER_DIR,
            image=image)

        self.build(dockerfile, image_tag)

    def build_all(self):
        images = os.listdir(directories.DOCKER_DIR)

        if images:
            info_log('Building Docker images: ' + ', '.join(images))

        for image in images:
            self.build_simple(image)
