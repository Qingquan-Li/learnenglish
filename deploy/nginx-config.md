> References:
> https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-20-04


# Configure Nginx to Proxy Pass to Gunicorn

After Gunicorn is set up, we need to configure Nginx to pass traffic to the process.

Start by creating and opening a new server block in Nginx’s sites-available directory:
```bash
$ sudo vim /etc/nginx/sites-available/learnenglish
```

Inside, open up a new server block. We will start by specifying that this block should `listen` on the normal port `80` and that it should respond to our server’s `domain name` or `IP address`.

Next, we will tell Nginx to ignore any problems with finding a `favicon`. We will also tell it where to find the `static` assets that we collected in our `~/myprojectdir/static` directory. All of these files have a standard URI prefix of “/static”, so we can create a location block to match those requests.

Finally, we’ll create a location / {} block to match all other requests. Inside of this location, we’ll include the standard `proxy_params` file included with the Nginx installation and then we will pass the traffic directly to the `Gunicorn socket`:
```
server {
    listen 80;
    server_name server_domain_or_IP;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/jake/learnenglish;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
```

Now, we can enable the file by linking it to the sites-enabled directory:
```bash
$ sudo ln -s /etc/nginx/sites-available/learnenglish /etc/nginx/sites-enabled
```

Test your Nginx configuration for syntax errors by typing:
```bash
$ sudo nginx -t
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
```

If no errors are reported, go ahead and restart Nginx by typing:
```bash
$ sudo systemctl restart nginx
```

If we have enabled ufw (uncomplicated firewall), we need to open up our firewall to normal traffic on port 80:
> References:
> https://www.digitalocean.com/community/tutorials/ufw-essentials-common-firewall-rules-and-commands
```bash
$ sudo ufw allow 'Nginx Full'
```
