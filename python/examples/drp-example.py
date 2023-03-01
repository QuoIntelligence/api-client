"""
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
"""

from quointelligence import QIClient

client = QIClient()

# ---------------------------------
# DRP tickets
tickets = client.drp(since="30d")  # from the last 30 days
"""
NOTE other possibilities:
tickets = client.drp(since='1h')   # 1 hour
tickets = client.drp(since='15m')  # 15 minutes
tickets = client.drp(since='40m')  # 40 days
tickets = client.drp(date_range=('2020-10-01', '2021-04-07'))
"""

print("DRP Tickets:")
for ticket in tickets:
    print(f"  {ticket['id']} {ticket['subject']}")

# ---------------------------------
# Ticket fetch more details
for ticket in client.drp(since="30d"):
    more = client.ticket(ticket["id"])
    print("\nTicket summary vs more detail:", ticket, more, sep="\n  ")
    break
else:
    print("no tickets matched that condition")

# ---------------------------------
# Intelligence tickets
tickets = client.intelligence(since="30d")  # from the last 30 days
print(f"\nCounted {len(list(tickets))} Intelligence tickets")
