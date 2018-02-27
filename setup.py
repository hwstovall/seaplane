from setuptools import setup

setup(name='seaplane',
      version='0.1',
      description='A simple tool to help get local Kubernetes projects up and running.',
      url='http://github.com/hwstovall/seaplane',
      author='hwstovall',
      author_email='hwstovall@gmail.com',
      license='MIT',
      install_requires=[
          'click',
          'colorama',
      ],
      include_package_data=True,
      pymodules=['seaplane.script'],
      entry_points='''
            [console_scripts]
            seaplane=seaplane.script:seaplane
      ''',
      zip_safe=False)
