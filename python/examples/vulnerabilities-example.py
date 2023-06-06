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

from quointelligence import QIClient

client = QIClient()

# Fetching vulnerabilities
try:
    vulnerabilities = client.catalogs("vulnerabilities")
    print("Found", len(vulnerabilities), "vulnerabilities in the catalog")
except ValueError as err:
    print(str(err))

# Fetching vulnerability alerts
alerts = list(client.vulnerability_alerts("7d"))
print("Found", len(alerts), "vulnerability alerts in the last 7 days")
for alert in alerts:
    print(" * ", alert["subject"])
