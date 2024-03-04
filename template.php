<?php
if (!isset($_SESSION['uuid'])) {
    header('HTTP/1.0 403 Forbidden');
    exit;
}
?>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
        "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="ru" lang="ru">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
    <meta http-equiv="Cache-Control" content="no-cache">
    <script type="text/javascript">
        function captcha_subm() {
            document.getElementById("captcha").submit()
        }
    </script>
    <style type="text/css">
        .error {
            color: #000;
            font-family: Arial, sans-serif;
            text-align: center;
            position: absolute;
            top: 50%;
            left: 50%;
            -moz-transform: translateX(-50%) translateY(-50%);
            -webkit-transform: translateX(-50%) translateY(-50%);
            transform: translateX(-50%) translateY(-50%);
        }

        .error-fon {
            font-weight: bold;
            color: #d0e3f7;
        }

        .error-text-top {
            font-size: 16px;
            color: #434141
        }

        hr {
            display: block;
            height: 10px;
            border: 0;
            border-top: 1px solid #ccc;
            margin: 1em 0;
            padding: 0;
        }
    </style>
    <title>403 Access denied</title>
    <script src="https://www.google.com/recaptcha/api.js" async defer></script>
</head>
<body>
<div class="error">
    <div class="error-fon">
        <font style="font-size:240px;">403</font>
        <br>
        <font style="font-size:40px;">ACCESS IS BLOCKED</font>
    </div>
    <br>
    <div class="error-text-wrap">
        <div class="error-text-top">
            <p>
            <hr>
            <p style="text-align: center;">
                Suspicious activity. To unblock your IP address please pass the CAPTCHA.
                <br><br>
                Подозрительная активность. Для разблокировки IP адреса пройдите проверку, используя функционал CAPTCHA.
            </p>
            <hr>
            <div style="width: 300px; margin: 0 auto;">

                <?php
                echo('<form action="?" method="POST" id="captcha">');
                echo('<div class="g-recaptcha" data-callback="captcha_subm" data-sitekey="' . settings::$SITE_KEY . '"></div>');
                echo('<br/>');
                echo('</form>');
                echo('</div>');
            ?>
            </div>
            </p>
        </div>

    </div>
</div>
</body>
</html>
