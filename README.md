# Traylert

![Traylert](https://github.com/IngoKl/Traylert/blob/master/data/logo.png?raw=true "Traylert")

*Beware: Since this tool has been initially developed for a very specific, on-off, edge case, the code quality is quite terrible! Feel free to improve the code! :)*

*Traylert* is an extremely simple monitoring/alerting system for individual machines.
Its name comes from the fact that the Trayler client runs in your Windows tray.

Traylert has three main functions:
- Providing very basic system information (from a server)
- Providing notifications and alerts via *Toast*
- Forwarding notifications from other applications (via a simple HTTP API)

![Traylert Infrastructure](https://github.com/IngoKl/Traylert/blob/master/data/traylert-infra.png?raw=true "Traylert Infrastructure")

In the simplest case, the client (local machine) just receives some basic information (e.g. free memory) from the server via HTTP. However, the server can also receive "alerts" (via HTTP POST) that are then downstreamed to the client and displaye via Windows Toast notications. 

Because SSL/TLS is not always available, the communication between the client and the server can be AES encrypted. While this, from a security standpoint, is not perfect, it should be sufficient for most use cases.

![Alert Example](https://github.com/IngoKl/Traylert/blob/master/data/alert-example.gif?raw=true "Alert Example")

## Configuration
Both the server and the client are configured trough a configuration file (`traylert.ini`).  Most importantly, you should set your own AES encryption key and adjust the whitelisted ips that can send alerts to the server.

## Deploying the Server
The Traylert server is implemented in *Flask*. The easiest way to get started is using *Gunicorn*.

`gunicorn -w 4 -b 127.0.0.1:4000 traylert.traylert_server:app`

This will start a server with four worker processes on port 4000.

For production (in which you should not use Traylert) you probably will want to have *NGINX* (or something else) in front of *Gunicorn*. Ideally, you will follow the "[Deploying Gunicorn](http://docs.gunicorn.org/en/stable/deploy.html "Deploying Gunicorn")" manual.

If you are collecting alerts from other machines, make sure to encrypt the HTTP traffic!

## Running the Client
You can run either run the clieht directly or install it via *pip*. After a simple `pip install .` in the root folder you should have `Traylert` available as a command. 

`Traylert --config-file custom.ini`
`Traylert --endpoint_override http://my-server.com:5000`

