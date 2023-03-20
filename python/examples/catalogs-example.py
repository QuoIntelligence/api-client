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

from collections import defaultdict
from quointelligence import QIClient

client = QIClient()

# Fetch all sectors
sectors = client.catalogs("sectors")

# Print results as an indented tree
children = defaultdict(list)
for sector in sectors:
    children[sector["id_parent"]].append(sector)


def printNode(sector: dict, margin=""):
    print(f"{margin}{sector['id']}: {sector['name']}")
    for child in children[sector["id"]]:
        printNode(child, margin + "    ")


print("Sectors:")
for top in children[0]:
    printNode(top)
