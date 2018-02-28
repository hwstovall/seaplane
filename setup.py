from setuptools import setup, find_packages

VERSION = '0.1.4'

setup(name='seaplane',
      version=VERSION,
      description='A simple tool to help get local Kubernetes projects up and running.',
      url='https://github.com/hwstovall/seaplane',
      download_url='https://github.com/hwstovall/seaplane/archive/{version}.tar.gz'.format(version=VERSION),
      author='hwstovall',
      author_email='hwstovall@gmail.com',
      license='MIT',
      install_requires=[
          'click',
          'colorama',
      ],
      include_package_data=True,
      packages=find_packages(),
      entry_points='''
            [console_scripts]
            seaplane=seaplane.script:seaplane
      ''',
      keywords=['kubernetes', 'minikube', 'development', 'docker', 'helm'],
      zip_safe=False)
