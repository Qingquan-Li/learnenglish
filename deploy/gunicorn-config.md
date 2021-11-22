> References:
> https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-20-04


# 1. Create and open a systemd socket file for Gunicorn

The Gunicorn socket will be created at boot and will listen for connections. When a connection occurs, systemd will automatically start the Gunicorn process to handle the connection.

```bash
$ sudo vim /etc/systemd/system/gunicorn.socket
```

Inside, we will create a [Unit] section to describe the socket,
a [Socket] section to define the socket location,
and an [Install] section to make sure the socket is created at the right time:

```
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target
```


# 2. Create and open a systemd service file for Gunicorn

The service filename should match the socket filename with the exception of the extension:

```bash
$ sudo vim /etc/systemd/system/gunicorn.service
```

Start with the [Unit] section, which is used to specify metadata and dependencies.
We’ll put a `Description` of our service here and tell the init system to only start this `After` the networking target has been reached. Because our service relies on the socket from the socket file, we need to include a `Requires` directive to indicate that relationship.

Next, we’ll open up the [Service] section. We’ll specify the `User` and `Group` that we want to process to run under. We will give our `regular user account` ownership of the process since it owns all of the relevant files. We’ll give group ownership to the `www-data` group so that Nginx can communicate easily with Gunicorn.
We’ll then map out the `working directory` and specify the command to use to start the service.
In this case, we’ll have to specify the full path to the `Gunicorn executable`, which is installed within our virtual environment.
We will `bind` the process to the Unix socket we created within the /run directory so that the process can communicate with Nginx.
We `log` all data to standard output so that the journald process can collect the Gunicorn logs.
We can also specify any optional Gunicorn tweaks here. For example, we specified 3 `worker` processes in this case.

Finally, we’ll add an [Install] section. This will tell systemd what to link this service to if we enable it to start at boot. We want this service to start when the regular multi-user system is up and running.

```
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=jake
Group=www-data
WorkingDirectory=/home/jake/learnenglish
ExecStart=/home/jake/learnenglish/.venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          a_project_config.wsgi:application

[Install]
WantedBy=multi-user.target
```

We can now start and enable the Gunicorn socket.
This will create the socket file at `/run/gunicorn.sock` now and at boot.
When a connection is made to that socket, systemd will automatically start the `gunicorn.service` to handle it:

```bash
$ sudo systemctl start gunicorn.socket
$ sudo systemctl enable gunicorn.socket
Created symlink /etc/systemd/system/sockets.target.wants/gunicorn.socket → /etc/systemd/system/gunicorn.socket.
```

We can confirm that the operation was successful by checking for the socket file.


# 3. Checking for the Gunicorn Socket File

Check the status of the process to find out whether it was able to start:
```bash
$ sudo systemctl status gunicorn.socket
● gunicorn.socket - gunicorn socket
     Loaded: loaded (/etc/systemd/system/gunicorn.socket; enabled; vendor preset: e>
     Active: active (listening) since Sat 2021-11-20 23:00:34 EST; 4min 36s ago
   Triggers: ● gunicorn.service
     Listen: /run/gunicorn.sock (Stream)
      Tasks: 0 (limit: 2245)
     Memory: 0B
     CGroup: /system.slice/gunicorn.socket

Nov 20 23:00:34 vm-ubuntu systemd[1]: Listening on gunicorn socket.
```

Next, check for the existence of the gunicorn.sock file within the /run directory:
```bash
$ file /run/gunicorn.sock
/run/gunicorn.sock: socket
```

If something goes wrong, Check the Gunicorn socket’s logs by typing:
```bash
$ sudo journalctl -u gunicorn.socket
-- Logs begin at Tue 2021-11-16 15:55:20 EST, end at Sat 2021-11-20 23:15:35 EST. --
Nov 20 23:00:34 vm-ubuntu systemd[1]: Listening on gunicorn socket.
```

# 4. Testing Socket Activation

Currently, if you’ve only started the gunicorn.socket unit, the gunicorn.service will not be active yet since the socket has not yet received any connections. You can check this by typing:
```bash
$ sudo systemctl status gunicorn
● gunicorn.service - gunicorn daemon
     Loaded: loaded (/etc/systemd/system/gunicorn.service; disabled; vendor preset:>
     Active: inactive (dead)
TriggeredBy: ● gunicorn.socket
```

To test the socket activation mechanism, we can send a connection to the socket through curl by typing:
```bash
$ curl --unix-socket /run/gunicorn.sock localhost
```

You should receive the HTML output from your application in the terminal. This indicates that Gunicorn was started and was able to serve your Django application. You can verify that the Gunicorn service is running by typing:

```bash
$ sudo systemctl status gunicorn
● gunicorn.service - gunicorn daemon
     Loaded: loaded (/etc/systemd/system/gunicorn.service; disabled; vendor preset:>
     Active: active (running) since Sat 2021-11-20 23:19:38 EST; 3min 52s ago
TriggeredBy: ● gunicorn.socket
   Main PID: 64050 (gunicorn)
      Tasks: 4 (limit: 2245)
     Memory: 101.2M
     CGroup: /system.slice/gunicorn.service
             ├─64050 /home/jake/learnenglish/.venv/bin/python3 /home/jake/learnengl>
             ├─64052 /home/jake/learnenglish/.venv/bin/python3 /home/jake/learnengl>
             ├─64053 /home/jake/learnenglish/.venv/bin/python3 /home/jake/learnengl>
             └─64054 /home/jake/learnenglish/.venv/bin/python3 /home/jake/learnengl>

Nov 20 23:19:38 vm-ubuntu systemd[1]: Started gunicorn daemon.
Nov 20 23:19:38 vm-ubuntu gunicorn[64050]: [2021-11-20 23:19:38 -0500] [64050] [INF>
Nov 20 23:19:38 vm-ubuntu gunicorn[64050]: [2021-11-20 23:19:38 -0500] [64050] [INF>
Nov 20 23:19:38 vm-ubuntu gunicorn[64050]: [2021-11-20 23:19:38 -0500] [64050] [INF>
Nov 20 23:19:38 vm-ubuntu gunicorn[64052]: [2021-11-20 23:19:38 -0500] [64052] [INF>
Nov 20 23:19:38 vm-ubuntu gunicorn[64053]: [2021-11-20 23:19:38 -0500] [64053] [INF>
Nov 20 23:19:38 vm-ubuntu gunicorn[64054]: [2021-11-20 23:19:38 -0500] [64054] [INF>
Nov 20 23:19:38 vm-ubuntu gunicorn[64053]: Not Found: /
Nov 20 23:19:38 vm-ubuntu gunicorn[64053]:  - - [20/Nov/2021:23:19:38 -0500] "GET />
```

If you make changes to the `/etc/systemd/system/gunicorn.service` file, reload the daemon to reread the service definition and restart the Gunicorn process by typing:
```bash
$ sudo systemctl daemon-reload
$ sudo systemctl restart gunicorn
```
