# QuoIntelligence Python Client

This is Python API Client module for QuoIntelligence API

```
from quointelligence import QIClient

client = QIClient('<user name>', '<password>')
tickets = client.drp(since='60d')  # get drp tickets in the past 60 days

ticket = client.ticket(1234)  # get ticket details of ticket with id 1234
```
