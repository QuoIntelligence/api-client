"""
Copyright 2023 QuoIntelligence GmbH
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    https://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from setuptools import setup

setup(
    name="quointelligence",
    version="0.1.0",
    description="Python client for Quointelligence API",
    url="https://github.com/QuoIntelligence/api-client/releases/tag/v0.1",
    author="Quointelligence GmbH",
    author_email="info@quointelligence.eu",
    license="Apache 2",
    packages=["quointelligence"],
    install_requires=[
        "requests",
        "python_dateutil",
    ],
    zip_safe=False,
)
