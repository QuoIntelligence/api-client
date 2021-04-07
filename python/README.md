# QuoIntelligence Python Client

This is the Python Client module for QuoIntelligence API.

# Setup

In your Python environment (preferrably a virtual one using `venv`), execute
this command:

```shell
pip install -e 'git+https://github.com/QuoIntelligence/api-client.git#egg=quointelligence&subdirectory=python'
```

# Documentation

`QIClient` is the main class of this package. To view its documentation, execute
the following in your Python shell:

```python
import quointelligence
help(quointelligence.client.QIClient)
```

# Example Usage

```python

from quointelligence import QIClient

client = QIClient('<user name>', '<password>')
tickets = client.drp(since='60d')  # get drp tickets in the past 60 days
ticket = client.ticket('1234')  # get ticket details of ticket with id 1234
```
