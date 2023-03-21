# QuoIntelligence API client
Quointelligence API client module(s)

## Licence
This project is licensed under the Apache License - see the [LICENSE file](/LICENSE) for details.

This is the Python Client module for QuoIntelligence API.

# Documentation 
The API is documented in this URL: https://mercury.quointelligence.eu/api/public/docs/index.html  
_(You must login first to https://mercury.quointelligence.eu)_

# Python Client implementation

In your Python environment (preferrably a virtual one using `venv`), execute
this command:

```shell
pip install -e \
  'git+https://github.com/QuoIntelligence/api-client.git#egg=quointelligence&subdirectory=python'
```

or for a specific version, eg `v0.1.0`:

```shell
pip install -e \
  'git+https://github.com/QuoIntelligence/api-client.git@v0.1.0#egg=quointelligence&subdirectory=python'
```

The `QIClient` is the main class of this package. To view its documentation, execute
the following in your Python shell:

```python
import quointelligence
help(quointelligence.client.QIClient)
```

# Example Usage

(also see the `python/example` folder)
```python

from quointelligence import QIClient

client = QIClient()
tickets = client.drp(since='60d')  # get drp tickets in the past 60 days
ticket = client.ticket('1234')  # get ticket details of ticket with id 1234
```

# Configuration

The `QIClient()` constructor accepts parameters directly, or from the environment.

Direct configuration:
```python
client = QIClient(
  url='https://mercury.quointelligence.eu/api/public',
  email='john.smith@example.com',
  password='<password>',
)
...
```

Environmental configuration:
```bash
export QI_API_URL='https://mercury.quointelligence.eu/api/public'
export QI_API_EMAIL='john.smith@example.com'
export QI_API_PASSWORD='<password>'
python my_script.py
```

