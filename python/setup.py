'''
Copyright 2021 QuoIntelligence GmbH
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    https://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

from setuptools import setup

setup(name='quointelligence',
      version='0-alpha',
      description='Python client for Quointelligence API',
      url='https://github.com/QuoIntelligence/api-client/tree/master/python',
      author='Quointelligence GmbH',
      author_email='info@quointelligence.eu',
      license='Apache 2',
      packages=['quointelligence'],
      install_requires=[
          'requests',
      ],
      zip_safe=False)
