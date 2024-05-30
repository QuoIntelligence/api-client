
> [!WARNING]
> The API this project references has been superseded.  
> For the latest information, please see
> https://mercury.quointelligence.eu/api/public/docs/index.html

# QuoIntelligence Public API 

QuoIntelligence provides a REST API for customer use.  
This API is documented, supported, and will not be changed without warning.

## Support

If you have any questions or difficulties with the API, contact your Customer Success representative.

## Getting Started

You will need a current user account to use the API.  
Not a customer yet? [Come and talk to us!](https://quointelligence.eu/)

The following examples demonstrate the barest way to access the API.  
This project includes a python client library for high-level access - see the [QuoIntelligence API client](#quointelligence-api-client) section below

## Authentication

### Getting a Token
Requests to the API need to be authenticated by an access token.  
There are two types of tokens:

1. You can generate a temporary token through the `login` endpoint by using your account credentials:

    ```bash
    # credentials.json contents:
    # {"email":"<your email address>","password":"<your password>"}

    curl -X POST 'https://mercury.quointelligence.eu/api/public/login' \
        -H 'Content-Type:application/json' \
        -H 'Accept:application/json' \
        -d @credentials.json

    # Expected output:
    # {"access_token":"..."}
    ```

2. You may request a permanent token - an **API Key**.  
    This key is associated with the user account, but is not impacted by 2FA or SAML requirements.

    **Note:** The API key must be kept secure! Contact us immediately if an API key needs to be removed or regenerated.

Both the above options are available to a normal user account.

You may also request a separate **service account**, if one is needed for production use.  


### Signing Requests
Once you have a token of either type, authorize your requests like:
```bash
TOKEN="..." # API key, or eg $(curl ...as above... | jq -r .access_token)

curl 'https://mercury.quointelligence.eu/api/public/intelligence?since=2023-06-01' \
    -H "Authorization: Bearer $TOKEN"
```

## API Documentation

Details of each endpoint in the public API can be found in the Swagger documentation:  
https://mercury.quointelligence.eu/api/public/docs/index.html

## Feature Requests?
We continue to work on improvements to the public API.

If you need a particular feature or aren't sure how to access particular data - just ask. 😉

&nbsp;

&nbsp;

&nbsp;






# QuoIntelligence API client

We provide a simple python library for interacting with the API.

## Installation

In your Python environment, run:

```shell
pip install -e 'git+https://github.com/QuoIntelligence/api-client.git#egg=quointelligence&subdirectory=python'
```

## Configuration

The `QIClient()` constructor can be configured directly, or with environment variables:

Direct configuration:
```python
client = QIClient(email='<your email address>', password='<your password>')
# OR
client = QIClient(key='<your API key>')
```

Environmental configuration:
```bash
export QI_API_EMAIL='<your email address>'
export QI_API_PASSWORD='<password>'
python my_script.py

# OR 

export QI_API_KEY='<your API key>'
python my_script.py
```

## Documentation

The `QIClient` is the main class of this package. Documentation can be viewed by running: _(in your Python shell)_

```python
from quointelligence import QIClient
help(QIClient)
```

## Example Usage

```python
from quointelligence import QIClient

client = QIClient()
tickets = client.drp(since='60d')  # get drp tickets in the past 60 days
ticket = client.ticket('1234')  # get ticket details of ticket with id 1234
```
See the `python/example` folder for more.

&nbsp;

&nbsp;

# License
The python client module for QuoIntelligence API is licensed under the Apache License - see the [LICENSE file](/LICENSE) for details.

