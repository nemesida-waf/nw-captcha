# nw-captcha
An example of PHP code for integrating Nemesida WAF with reCAPTCHA functionality (unblocking from IP addresses identified by Nemesida WAF as sources of DDoS, brute-force and flood attacks.

![Nemesida WAF with reCAPTCHA](https://camo.githubusercontent.com/e6c3083f740afe82447d5ab0a561f27a4e888a727619ef770ca2d5406290bd60/68747470733a2f2f7761662e70656e7465737469742e72752f77702d636f6e74656e742f75706c6f6164732f323032312f30322f3031342e706e67)

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
      sha_lic_key text,
      uuid        text,
      waf_id      text
  );

  create unique index client_uuid_uindex
      on client (uuid);
</pre>

Description of parameters:
<ul>
  <li><code>url</code> - the URL of the location with the option <code>nwaf_captcha_unban on;</code>;</li> 
 <li><code>sha_lic_key</code> - SHA1 licence key Nemesida WAF;</li> 
 <li><code>uuid</code> is a unique instance ID Nemesida WAF;</li> 
 <li><code>waf_id</code> - the ID of the group license keys.</li>
</ul>

The UUID and WAF ID are available in the Nginx service's <code>error.log</code> log.

Example:

<pre>
cat /var/log/nwaf/mla.log | grep -E 'UUID|WAF ID'</code>
2021-08-19 16:32:55,424 MLA_MOD_LOG  INFO     System UUID: xxxxxxxxxxxxxxxxxxxxx
2021-08-19 16:33:09,007 MLA_MOD_LOG  INFO     WAF ID: xxxxxxxxxxxxxxxxx
</pre>

![Init SQLite file](https://camo.githubusercontent.com/8abad87cd960159ac4271ef90e45ad210106db2a816805773d26922c9ffdd4d8/68747470733a2f2f696d672e646566636f6e2e72752f73746f72652f323032312f30392f38396232613466653536303435383332656131393131626135376239313033312e706e67)

Update the <code>DB_PATH</code> parameter to Settings.php .

## Activation
On a server with Nemesida WAF installed, in the settings <code>nwaf.conf</code> parameter <code>nwaf_ban_captcha_url</code>, determine the path to the server with the current PHP code. In NGINX settings, create a <code>location</code> with the <code>nwaf_captcha_unban on;</code> parameter so that <code>location</code> is available at the address specified in the <code>url</code> parameter of the SQLite file. For security reasons, we recommend restricting access to location only from the server running the current PHP code.
