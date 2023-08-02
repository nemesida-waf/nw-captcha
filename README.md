# nw-captcha
An example of PHP code for integrating Nemesida WAF with reCAPTCHA functionality (unblocking from IP addresses identified by Nemesida WAF as sources of DDoS, brute-force and flood attacks. <strong>nw-captcha</strong> along with configured Nginx is also available as a [Docker-image](https://hub.docker.com/repository/docker/nemesida/nw-captcha).

![Nemesida WAF with reCAPTCHA](https://user-images.githubusercontent.com/48731852/147060694-71a72241-e22a-488a-899e-d4befbe9f297.png)

## Get reCAPTCHA keys
In the control panel [Google reCAPTCHA](https://www.google.com/recaptcha/admin/) get the <code>site</code> and <code>secret</code> keys for reCAPTCHA v2 and make changes to the file <code>Settings.php</code>.

## Initiate the SQLite file:
Create an SQLite file, initiate its structure. Navigate to the directory where the file will be stored (for example, /opt/nw-captcha/) and create it:

<pre>
cd /opt/nw-captcha/
sqlite3 nw.db
</pre>

Create the required table:

<pre>
  create table client
  (
      url         text,
      token       text,
      uuid        text,
      waf_id      text
  );

  create unique index client_uuid_uindex
      on client (uuid);
</pre>

![Init SQLite file](https://user-images.githubusercontent.com/99513957/158990127-538199ca-1483-4039-a6d5-f10a64697012.png)

Description of parameters:
<ul>
  <li><code>url</code> - the URL of the location with the option <code>nwaf_captcha_unban on;</code>;</li>
 <li><code>token</code> - the value of the nwaf_ban_captcha_token parameter;</li>
 <li><code>uuid</code> is a unique instance ID Nemesida WAF;</li>
 <li><code>waf_id</code> - the ID of the group license keys.</li>
</ul>

Add records to the database for each server with Nemesida WAF.

Example:
<pre>INSERT INTO client(url, token, uuid, waf_id) VALUES ("https://example.ru/captcha_unban","token","uuid","waf_id");</pre>

The UUID and WAF ID are available in the Nginx service's <code>error.log</code> log.

Example:
<pre>
# cat /var/log/nginx/error.log | grep 'WAF ID'

2022/01/01 00:00:00 [info] ...: Nemesida WAF: UUID: XXX; WAF ID: XXX. ...
</pre>

Update the <code>DB_PATH</code> parameter to Settings.php .

## Activation
On a server with Nemesida WAF installed, in the settings <code>nwaf.conf</code>, set the parameters <code>nwaf_ban_captcha_url</code>, which defines the path to the server with the current PHP code and <code>nwaf_ban_captcha_token</code>, which defines the secret string for unlocking the IP address. In NGINX settings, create a <code>location</code> with the <code>nwaf_captcha_unban on;</code> parameter so that <code>location</code> is available at the address specified in the <code>url</code> parameter of the SQLite file. For security reasons, we recommend restricting access to location only from the server running the current PHP code.

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

6. Install <code>SQLite3</code> and make configuration changes.

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
