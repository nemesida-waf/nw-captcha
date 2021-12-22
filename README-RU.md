# nw-captcha
Пример PHP-кода для интеграции Nemesida WAF с функционалом reCAPTCHA (снятие блокировки с IP-адресов, определенных Nemesida WAF как источники DDoS, атак методом перебора и флуда.

![Nemesida WAF with reCAPTCHA](https://camo.githubusercontent.com/e6c3083f740afe82447d5ab0a561f27a4e888a727619ef770ca2d5406290bd60/68747470733a2f2f7761662e70656e7465737469742e72752f77702d636f6e74656e742f75706c6f6164732f323032312f30322f3031342e706e67)

## Получите ключи reCAPTCHA
В панели управления [Google reCAPTCHA](https://www.google.com/recaptcha/admin/) получите SITE/SECRET ключи для reCAPTCHA v2 и внестите изменения в файл Settings.php.

## Инициируйте файл SQLite:
Создайте файл SQLite, инициируйте его структуру. Перейдите в каталог, где будет храниться файл (например, /var/www), и создайте его:

<pre>
cd /var/www/
sqlite nw.db
</pre>

Создайте необходимую таблицу:

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

Описание параметров:
<ul>
  <li><code>url</code> - URL location с включенной опцией <code>nwaf_captcha_unban on;</code>;</li>
  <li><code>sha_lic_key</code> - SHA1 от лицензионного ключа Nemesida WAF;</li>
  <li><code>uuid</code> - уникальный идентификатор экземпляра Nemesida WAF;</li>
  <li><code>waf_id</code> - идентификатор группы лицензионных ключей.</li>
</ul>

UUID и WAF ID доступны в журнале <code>error.log</code> сервиса Nginx.

Пример:

<pre>
cat /var/log/nwaf/mla.log | grep -E 'UUID|WAF ID'</code>
2021-08-19 16:32:55,424 MLA_MOD_LOG  INFO     System UUID: xxxxxxxxxxxxxxxxxxxxx
2021-08-19 16:33:09,007 MLA_MOD_LOG  INFO     WAF ID: xxxxxxxxxxxxxxxxx
</pre>

![Init SQLite file](https://camo.githubusercontent.com/8abad87cd960159ac4271ef90e45ad210106db2a816805773d26922c9ffdd4d8/68747470733a2f2f696d672e646566636f6e2e72752f73746f72652f323032312f30392f38396232613466653536303435383332656131393131626135376239313033312e706e67)

Обновите параметр <code>DB_PATH</code> в Settings.php.

## Активация
На сервере с установленным Nemesida WAF в настройках <code>nwaf.conf</code> параметром <code>nwaf_ban_captcha_url</code> определите путь до сервера с текущим PHP-кодом. В настройках NGINX создайте <code>location</code> с параметром <code>nwaf_captcha_unban on;</code> таким образом, чтобы <code>location</code> был доступен по адресу, указанному в параметр <code>url</code> файла SQLite. В целях безопасности рекомендуем ограничить доступ к location только с сервера, на котором запущен текущий PHP-код.
