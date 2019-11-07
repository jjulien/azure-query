# Azure Query
This is both a python library and CLI tool that can be used to query the Microsft Graph REST API v1.0.  It can be used as a CLI to construct calls that directly map to a single call to the Graph API, and receive the JSON response.  It can also be used as a library to create your own utilities if you have more complex use cases.

## Overview
The tool utilizes a local web browser to perform an OAuth challenge and retrieve an access token.  This makes the flow interactive by default.  It caches the access token under `$HOME/.aq/token` for future calls while the token is still valid.

Currently the tool is only supported on OSX and requires Python 3.

## Usage
The CLI command `aq` is used to make calls out to the Graph API.  It currently only support GET operations.  It is a straight passthrough to the endpoint found in the [Microsoft Graph API v1.0 reference](https://docs.microsoft.com/en-us/graph/api/overview?view=graph-rest-1.0).

The CLI also supports the [OData Query Options](https://docs.microsoft.com/en-us/graph/query-parameters#odata-system-query-options) via CLI flags.

Example:
```
$ aq get /users --filter "startsWith(displayName,'Example')"
{
    "@odata.context": "https://graph.microsoft.com/v1.0/$metadata#users",
    "value": [
        {
            "businessPhones": [],
            "displayName": "Example1 User",
            "givenName": null,
            "jobTitle": null,
            "mail": null,
            "mobilePhone": null,
            "officeLocation": null,
            "preferredLanguage": null,
            "surname": null,
            "userPrincipalName": "example1@example.onmicrosoft.com",
            "id": "2ba42c9f-2055-45ce-9cd1-5b4244809bb1"
        },
        {
            "businessPhones": [],
            "displayName": "Example2 User",
            "givenName": null,
            "jobTitle": null,
            "mail": null,
            "mobilePhone": null,
            "officeLocation": null,
            "preferredLanguage": null,
            "surname": null,
            "userPrincipalName": "example@directoryspot.onmicrosoft.com",
            "id": "3c78c8dd-5b27-4f63-f894-54e971f313e3"
        }
    ]
}
```
