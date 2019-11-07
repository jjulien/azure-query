# Azure Active Directory Query Tool
**NOTE**: This tool is still in a very early development state, and patterns of usage will likely change as the tool matures.

## Overview
This tool provides both a CLI utility and python library that can be used to make queries against Microsoft Active Directory.  It utilizes the Graph API endpoint.

## Usage
The tool currently supports any http `GET` operation against the Graph API v1.0.  The CLI utility will automatically prompt the user for login credentials via the default browser, and will cache these credentials for as long as they are valid.

Example Usage:
```
#aq me
Currently Logged in as john@julienfamily.com
{"@odata.context":"https://graph.microsoft.com/v1.0/$metadata#users/$entity","displayName":"John Julien","surname":"Julien","givenName":"John","id":"e39240df98dc3","userPrincipalName":"john@julienfamily.com","businessPhones":[],"jobTitle":null,"mail":null,"mobilePhone":null,"officeLocation":null,"preferredLanguage":null}
```


