# nw-captcha
Пример PHP-кода для интеграции Nemesida WAF с функционалом reCAPTCHA (снятие блокировки с IP-адресов, определенных Nemesida WAF как источники DDoS, атак методом перебора и флуда). <strong>nw-captcha</strong> вместе с настроенным Nginx доступен также в виде [Docker-образа](https://hub.docker.com/repository/docker/nemesida/nw-captcha).

![Nemesida WAF with reCAPTCHA](https://camo.githubusercontent.com/e6c3083f740afe82447d5ab0a561f27a4e888a727619ef770ca2d5406290bd60/68747470733a2f2f7761662e70656e7465737469742e72752f77702d636f6e74656e742f75706c6f6164732f323032312f30322f3031342e706e67)

## Получите ключи reCAPTCHA
В панели управления [Google reCAPTCHA](https://www.google.com/recaptcha/admin/) получите <code>site</code> и <code>secret</code> ключи для reCAPTCHA v2 и внестите изменения в файл <code>settings.php</code>.

## Инициируйте файл SQLite:
Создайте файл SQLite, инициируйте его структуру. Перейдите в каталог, где будет храниться файл (например, /opt/nw-captcha/), и создайте его:

<pre>
mkdir -p /opt/nw-captcha/
sqlite3 /opt/nw-captcha/nw.db
</pre>

Создайте необходимую таблицу:

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

Описание параметров:
<ul>
  <li><code>url</code> - URL-адрес сервера с установленным динамическим модулем Nemesida WAF (в формате СХЕМА://АДРЕС СЕРВЕРА[:ПОРТ]);</li>
  <li><code>token</code> - значение параметра nwaf_ban_captcha_token;</li>
  <li><code>uuid</code> - уникальный идентификатор экземпляра Nemesida WAF;</li>
  <li><code>waf_id</code> - идентификатор группы лицензионных ключей.</li>
</ul>

![Init SQLite file](https://user-images.githubusercontent.com/99513957/158990127-538199ca-1483-4039-a6d5-f10a64697012.png)

Добавьте в базу данных записи для каждого используемого сервера с Nemesida WAF.

Пример:
<pre>INSERT INTO client(url, token, uuid, waf_id) VALUES ("https://example.ru","token","uuid","waf_id");</pre>

UUID и WAF ID доступны в журнале <code>error.log</code> сервиса Nginx.

Пример:
<pre>
# cat /var/log/nginx/error.log | grep 'WAF ID'

2022/01/01 00:00:00 [info] ...: Nemesida WAF: UUID: XXX; WAF ID: XXX. ...
</pre>

Обновите параметр <code>DB_PATH</code> в <code>settings.php</code>.

## Активация
На сервере с установленным Nemesida WAF в настройках <code>nwaf.conf</code> установите параметр <code>nwaf_ban_captcha_token</code>, который определяет строку-секрет для разблокировки IP-адреса.

<hr>

## Docker-образ

### Развертывание Docker-контейнера с nw-captcha

Для развертывания контейнера с <code>nw-captcha</code> необходимо выполнить следующие действия:<br>
1. Загрузите образ, содержащий <code>nw-captcha</code> вместе с настроенным Nginx:<br>
<pre># docker pull nemesida/nw-сaptcha</pre>

2. Создайте каталог:
<pre># mkdir -p /opt/nwaf/nw-captcha</pre>

3. В каталоге конфигурационных файлов создайте файл <code>first-launch</code>:
<pre># touch /opt/nwaf/nw-captcha/first-launch</pre>

4. Запустите контейнер с <code>nw-captcha</code>, используя команды:
<pre>
# iptables -t filter -N DOCKER
# docker run --rm -d -v /opt/nwaf/nw-captcha:/nw-captcha -p 80:80 nemesida/nw-сaptcha
</pre>

где:
<ul>
	<li><code>--rm</code> - удаление контейнера после завершения работы;</li>
	<li><code>-d</code> - запуск контейнера в фоновом режиме;</li>
	<li><code>/opt/nwaf/nw-captcha:/nw-captcha</code> - монтирование каталога с конфигурационными файлами внутрь контейнера;</li>
	<li><code>-p 80:80</code> - проброс порта <code>80</code> контейнера на внешний порт <code>80</code>.</li>
</ul>

Посмотреть ID контейнера (cтолбец CONTAINER ID) можно командой:
<pre># docker ps -a</pre>

Остановить контейнер можно командой:
<pre># docker stop /ID контейнера/</pre>

5. Разрешите доступ на чтение для всех для каталога <code>nw-captcha</code>:
<pre># chmod -R 0555 /opt/nwaf/nw-captcha</pre>

6. Установите <code>SQLite3</code> и внесите изменения в конфигурацию.

7. Для запуска контейнера выполните следующие команды:
<pre>
# iptables -t filter -N DOCKER
# docker run --rm -d -v /opt/nwaf/nw-captcha:/nw-captcha -p 80:80 nemesida/nw-сaptcha
</pre>

где:
<ul>
	<li><code>--rm</code> - удаление контейнера после завершения работы;</li>
	<li><code>-d</code> - запуск контейнера в фоновом режиме;</li>
	<li><code>/opt/nwaf/nw-captcha:/nw-captcha</code> - монтирование каталога с конфигурационными файлами внутрь контейнера;</li>
	<li><code>-p 80:80</code> - проброс порта <code>80</code> контейнера на внешний порт <code>80</code>.</li>
</ul>

### Обновление Docker-образа
1. Перед обновлением образа <code>nw-captcha</code> проверьте, запущен ли контейнер. Для этого необходимо посмотреть ID контейнера (cтолбец CONTAINER ID), используя команду:<br>
<pre># docker ps -a</pre>

2. Если контейнер запущен, остановите его, используя команду:
<pre># docker stop /ID контейнера/</pre>

3. При остановленном контейнере удалите образ:
<pre># docker image rm nemesida/nw-captcha</pre>

4. Загрузите образ, содержащий <code>nw-captcha</code>:
<pre># docker pull nemesida/nw-captcha</pre>

5. Запустите контейнер с образом <code>nw-captcha</code>, используя команду:
<pre>
# iptables -t filter -N DOCKER
# docker run --rm -d -v /opt/nwaf/nw-captcha/:/nw-captcha nemesida/nw-captcha
</pre>
