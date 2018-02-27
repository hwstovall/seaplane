from setuptools import setup

setup(name='seaplane',
      version='0.1.2',
      description='A simple tool to help get local Kubernetes projects up and running.',
      url='https://github.com/hwstovall/seaplane',
      download_url='https://github.com/hwstovall/seaplane/archive/0.1.2.tar.gz',
      author='hwstovall',
      author_email='hwstovall@gmail.com',
      license='MIT',
      install_requires=[
          'click',
          'colorama',
      ],
      include_package_data=True,
      packages=['seaplane'],
      entry_points='''
            [console_scripts]
            seaplane=seaplane.script:seaplane
      ''',
      keywords=['kubernetes', 'minikube', 'development', 'docker', 'helm'],
      zip_safe=False)
