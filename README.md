# Simple TLS connection

## Setup

This code was implemented using Ubuntu 22.04 (WSL) with Python 3.10.6

To run this program it is necessary to import SymPy Library:

Open the terminal and enter the following command:
```bash
$ sudo apt install python3-sympy 
```

## Generate the certificate and private key

Open the terminal and enter the following commands:

```bash
$ openssl req -new -x509 -days 365 -nodes -out cert.pem -keyout key.pem -subj "/C=DK/ST=Sjaelland/L=Copenhagen/O=ITU/OU=ITU/CN=example.org/emailAddress=ades@itu.dk"
```

Certificate Parameters Explained:

- **C**, which is a 2 letter code for a country;
- **ST**, which is a state or province name;
- **L** *(optional)*, which is a city name;
- **O**, which is an organization name;
- **OU** *(optional)*, which is an organizational unit name;
- **CN**, which is the hostname:
  - **Warning** If you change the **CN** value, you have to change the hostname under [client.py](client.py) to reflect the new hostname.
- **emailAddress** *(optional)*, which is an email address.

## Running the TLS connection example

### Run the server example

Open the terminal and enter the following commands:

```bash
$ python3 server.py
```

### Run the client example

Open the terminal and enter the following commands:

```bash
$ python3 client.py
```
