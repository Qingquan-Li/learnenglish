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
     Loaded: loaded (/etc/systemd/system/gunicorn.socket; enabled; vendor preset: enabled)
     Active: active (listening) since Mon 2021-11-22 02:42:02 UTC; 57s ago
   Triggers: ● gunicorn.service
     Listen: /run/gunicorn.sock (Stream)
      Tasks: 0 (limit: 1136)
     Memory: 0B
     CGroup: /system.slice/gunicorn.socket

Nov 22 02:42:02 ubuntu systemd[1]: Listening on gunicorn socket.
```

Next, check for the existence of the gunicorn.sock file within the /run directory:
```bash
$ file /run/gunicorn.sock
/run/gunicorn.sock: socket
```

If something goes wrong, Check the Gunicorn socket’s logs by typing:
```bash
$ sudo journalctl -u gunicorn.socket
-- Logs begin at Tue 2021-11-02 02:21:52 UTC, end at Mon 2021-11-22 02:44:44 UTC. --
Nov 22 02:42:02 ubuntu systemd[1]: Listening on gunicorn socket.
```

# 4. Testing Socket Activation

Currently, if you’ve only started the gunicorn.socket unit, the gunicorn.service will not be active yet since the socket has not yet received any connections. You can check this by typing:
```bash
$ sudo systemctl status gunicorn
● gunicorn.service - gunicorn daemon
     Loaded: loaded (/etc/systemd/system/gunicorn.service; disabled; vendor preset: enabled)
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
     Loaded: loaded (/etc/systemd/system/gunicorn.service; disabled; vendor preset: enabled)
     Active: active (running) since Mon 2021-11-22 02:47:10 UTC; 53s ago
TriggeredBy: ● gunicorn.socket
   Main PID: 231768 (gunicorn)
      Tasks: 4 (limit: 1136)
     Memory: 102.7M
     CGroup: /system.slice/gunicorn.service
             ├─231768 /home/jake/learnenglish/.venv/bin/python3 /home/jake/learnenglish/.venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/run/gunicorn.sock a_project_config.sock a_project_config.wsgi:application
             ├─231780 /home/jake/learnenglish/.venv/bin/python3 /home/jake/learnenglish/.venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/run/gunicorn.sock a_project_config.sock a_project_config.wsgi:application
             ├─231781 /home/jake/learnenglish/.venv/bin/python3 /home/jake/learnenglish/.venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/run/gunicorn.sock a_project_config.sock a_project_config.wsgi:application
             └─231782 /home/jake/learnenglish/.venv/bin/python3 /home/jake/learnenglish/.venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/run/gunicorn.sock a_project_config.sock a_project_config.wsgi:application

Nov 22 02:47:10 ubuntu systemd[1]: Started gunicorn daemon.
Nov 22 02:47:10 ubuntu gunicorn[231768]: [2021-11-22 02:47:10 +0000] [231768] [INFO] Starting gunicorn 20.1.0
Nov 22 02:47:10 ubuntu gunicorn[231768]: [2021-11-22 02:47:10 +0000] [231768] [INFO] Listening at: unix:/run/gunicorn.sock (231768)
Nov 22 02:47:10 ubuntu gunicorn[231768]: [2021-11-22 02:47:10 +0000] [231768] [INFO] Using worker: sync
Nov 22 02:47:10 ubuntu gunicorn[231780]: [2021-11-22 02:47:10 +0000] [231780] [INFO] Booting worker with pid: 231780
Nov 22 02:47:10 ubuntu gunicorn[231781]: [2021-11-22 02:47:10 +0000] [231781] [INFO] Booting worker with pid: 231781
Nov 22 02:47:10 ubuntu gunicorn[231782]: [2021-11-22 02:47:10 +0000] [231782] [INFO] Booting worker with pid: 231782
Nov 22 02:47:11 ubuntu gunicorn[231780]:  - - [21/Nov/2021:21:47:11 -0500] "GET / HTTP/1.1" 404 179 "-" "curl/7.68.0"
```

If you make changes to the `/etc/systemd/system/gunicorn.service` file, reload the daemon to reread the service definition and restart the Gunicorn process by typing:
```bash
$ sudo systemctl daemon-reload
$ sudo systemctl restart gunicorn
```
