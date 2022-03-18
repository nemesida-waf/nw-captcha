# nw-captcha
An example of PHP code for integrating Nemesida WAF with reCAPTCHA functionality (unblocking from IP addresses identified by Nemesida WAF as sources of DDoS, brute-force and flood attacks.

![Nemesida WAF with reCAPTCHA](https://user-images.githubusercontent.com/48731852/147060694-71a72241-e22a-488a-899e-d4befbe9f297.png)

## Get reCAPTCHA keys
In the control panel [Google reCAPTCHA](https://www.google.com/recaptcha/admin/) get the SITE/SECRET keys for reCAPTCHA v2 and make changes to the file Settings.php .

## Initiate the SQLite file:
Create an SQLite file, initiate its structure. Navigate to the directory where the file will be stored (for example, /var/www) and create it:

<pre>
cd /var/www/
sqlite nw.db
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

Description of parameters:
<ul>
  <li><code>url</code> - the URL of the location with the option <code>nwaf_captcha_unban on;</code>;</li>
 <li><code>token</code> - the value of the nwaf_ban_captcha_token parameter;</li>
 <li><code>uuid</code> is a unique instance ID Nemesida WAF;</li>
 <li><code>waf_id</code> - the ID of the group license keys.</li>
</ul>

The UUID and WAF ID are available in the Nginx service's <code>error.log</code> log.

Example:

<pre>
# cat /var/log/nginx/error.log | grep 'WAF ID'

2022/01/01 00:00:00 [info] ...: Nemesida WAF: UUID: XXX; WAF ID: XXX. ...
</pre>

![Init SQLite file](https://camo.githubusercontent.com/8abad87cd960159ac4271ef90e45ad210106db2a816805773d26922c9ffdd4d8/68747470733a2f2f696d672e646566636f6e2e72752f73746f72652f323032312f30392f38396232613466653536303435383332656131393131626135376239313033312e706e67)

Update the <code>DB_PATH</code> parameter to Settings.php .

## Activation
On a server with Nemesida WAF installed, in the settings <code>nwaf.conf</code>, set the parameters <code>nwaf_ban_captcha_url</code>, which defines the path to the server with the current PHP code and <code>nwaf_ban_captcha_token</code>, which defines the secret string for unlocking the IP address. In NGINX settings, create a <code>location</code> with the <code>nwaf_captcha_unban on;</code> parameter so that <code>location</code> is available at the address specified in the <code>url</code> parameter of the SQLite file. For security reasons, we recommend restricting access to location only from the server running the current PHP code.
