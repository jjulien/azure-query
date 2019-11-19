import setuptools, os

long_description = """
This is a CLI utility and pythong library for interacting with the Microsfot Graph REST API v1.0.

It provides a thin wrapper, that essentially makes REST calls to the Graph API and returns the JSON result.
It can be used as a library to create your own custom python tools that query the Graph API, and it also
comes with the executable `aq` which allows you to run queries from the command line.

It requires OAuth for access to the API, and will utilize a local web browser to obtain an access token.

Details on the Graph API v1.0 can be found on Microsoft's site
https://docs.microsoft.com/en-us/graph/api/overview?view=graph-rest-1.0
"""

setuptools.setup(
    name="azure-query",
    version="0.0.3",
    scripts=["bin/aq"],
    author="John Julien",
    author_email="john@julinfamily.com",
    description="Command Line utility to query Azure AD",
    long_description=long_description,
    long_description_content_type="text/plain",
    url="https://github.com/jjulien/azure-query",
    packages=setuptools.find_packages('src'),
    package_data={'aq': ['auth_landing_pages/*.html']},
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS :: MacOS X"
    ],
    install_requires=[
        "PyJWT",
        "requests",
        "cryptography",
        "six"
    ]
) 
