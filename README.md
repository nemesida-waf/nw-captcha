# Nemesida WAF CAPTCHA
An example of Python/FastAPI code for integrating Nemesida WAF with CAPTCHA functionality. <strong>Nemesida WAF CAPTCHA</strong> is also available as a [Docker-image](https://hub.docker.com/repository/docker/nemesida/nw-captcha).

![Nemesida WAF CAPTCHA](https://user-images.githubusercontent.com/48731852/147060694-71a72241-e22a-488a-899e-d4befbe9f297.png)

## Quick start

<pre>
# apt update && apt install -y nginx python3 python3-venv python3-pip memcached
# python3 -m venv /var/www/nw-captcha/venv
# /var/www/nw-captcha/venv/bin/python3 -m pip install --upgrade pip
# /var/www/nw-captcha/venv/bin/python3 -m pip install -r /var/www/nw-captcha/requirements.txt
# cd /var/www/
# git clone https://github.com/nemesida-waf/nw-captcha
# cp /var/www/nw-captcha/db.json.example /var/www/nw-captcha/db.json
# mkdir -p /var/log/nwaf/captcha
# chmod -R 0750 /var/log/nwaf/captcha
# chown -R www-data:www-data /var/log/nwaf/captcha
# cp /var/www/nw-captcha/misc/captcha /etc/logrotate.d/
# cp /var/www/nw-captcha/misc/captcha.service /lib/systemd/system/
</pre>

Update /var/www/nw-captcha/db.json with data:

<ul>
  <li><code>token</code> - the secret token;</li>
  <li><code>uuid</code> - a unique Nemesida WAF instance ID;</li>
  <li><code>url</code> - URL of the server with the Nemesida WAF dynamic module installed (<code>SCHEMA://HOST[:PORT][/PATH]</code>).</li>
</ul>

An example:

<pre>
[
    {
        "token": "Abcdefg1",
        "uuid": "283fdec1fc7e9caa7595cdd4956a5c38",
        "url": "http://example.com"
    },
    {
        "token": "Acdefg2",
        "uuid": "393fdec1fc7e9caa7595cdd4956a5c39",
        "url": "http://example.com"
    }
]
</pre>

The UUID and WAF ID are available in the Nginx service's <code>error.log</code> log, e.g.:

<pre>
# cat /var/log/nginx/error.log | grep 'WAF ID'

2022/01/01 00:00:00 [info] ...: Nemesida WAF: UUID: XXX; WAF ID: XXX. ...
</pre>

Optional. Update the <code>proxy</code> parameter in <code>settings.php</code> (e.g. <code>proxy = 'http://proxy.example.com:3128'</code>).

## Start the CAPTCHA

Start the CAPTCHA:

<pre>
# systemctl enable captcha
# systemctl start captcha
</pre>

Check CAPTCHA status and logs:

<pre>
# systemctl status captcha
# cat /var/log/nwaf/captcha/api.log
# netstat -nlp | grep 8080
</pre>

CAPTCHA will listen on <code>8080</code> port.

## Enable CAPTCHA
Enable CAPTCHA in Nemesida WAF with Cabinet or API.

## Keep your enviroment up-to-date

It is important to keep your environment updated:
<pre>
# apt update && apt upgrade -y
# /var/www/nw-captcha/venv/bin/python3 -m pip install --upgrade pip
# /var/www/nw-captcha/venv/bin/python3 -m pip install --upgrade wheel
# /var/www/nw-captcha/venv/bin/python3 -m pip freeze | sed -r 's|==.+||' > /tmp/requirements.txt
# /var/www/nw-captcha/venv/bin/python3 -m pip install --upgrade -r /tmp/requirements.txt
# systemctl restart captcha
</pre>

<hr>

## Docker image

### Docker container deploying

To deploy a container with <code>nw-captcha</code>, follow these steps:<br>
1. Upload an image containing <code>nw-captcha</code> along with the configured Nginx:<br>
<pre># docker pull nemesida/nw-captcha</pre>

2. Create a directory:
<pre># mkdir -p /opt/nwaf/nw-captcha</pre>

3. In the configuration files directory, create a file <code>first-launch</code>:
<pre># touch /opt/nwaf/nw-captcha/first-launch</pre>

4. Launch the container with <code>nw-captcha</code> using the commands:

<pre>
# iptables -t filter -N DOCKER
# docker run --rm -d -v /opt/nwaf/nw-captcha:/nw-captcha -p 80:80 nemesida/nw-captcha
</pre>

where:
<ul>
<li><code>--rm</code> - deleting the container after completion of work;</li>
<li><code>-d</code> - running the container in the background;</li>
<li><code>/opt/nwaf/nw-captcha:/nw-captcha</code> - mounting a directory with configuration files inside the container;</li>
<li><code>-p 80:80</code> - port forwarding <code>80</code> of the container to the external port <code>80</code>.</li>
</ul>

To view the container ID (the CONTAINER ID column), you can use the command:
<pre># docker ps -a</pre>

You can stop the container with the command:
<pre># docker stop /container ID/</pre>

5. Allow read access for everyone for the <code>nw-captcha</code> directory:
<pre># chmod -R 0555 /opt/nwaf/nw-captcha</pre>

6. Setting up the files:
<ul>
    <li>/opt/nwaf/nw-captcha/db.json</li>
    <li>/opt/nwaf/nw-captcha/settings.py (optional)</li>
</ul>

7. To launch the container, run the following commands:
<pre>
# iptables -t filter -N DOCKER
# docker run --rm -d -v /opt/nwaf/nw-captcha:/nw-captcha -p 80:80 nemesida/nw-captcha
</pre>

where:
<ul>
<li><code>--rm</code> - deleting the container after completion of work;</li>
<li><code>-d</code> - running the container in the background;</li>
<li><code>/opt/nwaf/nw-captcha:/nw-captcha</code> - mounting a directory with configuration files inside the container;</li>
<li><code>-p 80:80</code> - port forwarding <code>80</code> of the container to the external port <code>80</code>.</li>
</ul>

### Docker image updating
1. Before updating the image <code>nw-captcha</code>, check whether the container is running. To do this, you need to view the container ID (the CONTAINER ID column) using the command:<br>
<pre># docker ps -a</pre>

2. If the container is running, stop it using the command:
<pre># docker stop /container ID/</pre>

3. When the container is stopped, delete the image:
<pre># rm docker image nemesida/nw-captcha</pre>

4. Upload an image containing <code>nw-captcha</code>:
<pre># docker pull nemesida/nw-captcha</pre>

5. Launch the container with the image <code>nw-captcha</code> using the command:
<pre>
# iptables -t filter -N DOCKER
# docker run --rm -d -v /opt/nwaf/nw-captcha/:/nw-captcha nemesida/nw-captcha
</pre>
