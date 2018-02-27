from abc import ABCMeta, abstractmethod


class BaseConfig(meta=ABCMeta):
    NAMESPACE = 'default'

    MINIKUBE_PORT_RANGE = None
    MINIKUBE_FLAGS = None

    @property
    @abstractmethod
    def MINIKUBE_PROJECT_PATH(self) -> str:
        pass

