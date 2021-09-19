<?php
session_start();
require_once "Settings.php";
require_once "DB.php";
require_once "nwaf_dyn_captcha.php";

$url = '';
$args = '';
$vhost = '';
$uuid = '';
$ip = '';

$db = DB::getInstance();

if (isset($_SESSION['uuid'])) {
    if (isset($_POST['g-recaptcha-response'])) {

        $clients_param = $db->get_para_by_db($_SESSION['uuid']);
        $url_captcha_ch = "https://www.google.com/recaptcha/api/siteverify";
        $key = Settings::$SECRET_KEY;
        $query = array(
            "secret" => $key,
            "response" => $_POST['g-recaptcha-response'],
            "remoteip" => $_SERVER['REMOTE_ADDR']
        );

        $ch = curl_init();

        curl_setopt($ch, CURLOPT_URL, $url_captcha_ch);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_POST, true);
        if (Settings::$PROXY != '') {
            curl_setopt($ch, CURLOPT_PROXY, Settings::$PROXY);
        }
        curl_setopt($ch, CURLOPT_POSTFIELDS, $query);

        $data = json_decode(curl_exec($ch), $assoc = true);
        curl_close($ch);
        if ($data['success'] == true) {
            if ($_SESSION['ip'] != '') {
                foreach ($clients_param as $client_param) {
                    unblockIP($_SESSION['ip'], $client_param['url'], $client_param['sha_lic_key'], Settings::$PROXY);
                }
            } else {
                foreach ($clients_param as $client_param) {
                    unblockIP($_SERVER['REMOTE_ADDR'], $client_param['url'], $client_param['sha_lic_key'], Settings::$PROXY);
                }
            }
            sleep(5);
            header("Location: https://" . $_SESSION['vhost'] . $_SESSION['url'] . "/?" . $_SESSION['args']);
            $_SESSION['url'] = '';
            $_SESSION['vhost'] = '';
            $_SESSION['args'] = '';
            $_SESSION['uuid'] = '';
            $_SESSION['ip'] = '';
            exit(0);
        }
    }
}
if (isset($_REQUEST['url'])) {
    $url = base64_decode($_REQUEST['url'], true);
    if ($url == false) {
        $url = '/';
    }
}
if (isset($_REQUEST['args'])) {
    $args = base64_decode($_REQUEST['args'], true);
    if ($args == false) {
        $args = '';
    }
}
if (isset($_REQUEST['vhost'])) {
    $vhost = base64_decode($_REQUEST['vhost'], true);
    if ($vhost == false) {
        $vhost = '';
    }
}
if (isset($_REQUEST['uuid'])) {
    $uuid = base64_decode($_REQUEST['uuid'], true);
    if ($uuid == false) {
        $uuid = '';
    }
}
if (isset($_REQUEST['ip'])) {
    $ip = base64_decode($_REQUEST['ip'], true);
    if ($ip == false) {
        $ip = '';
    }
}

if ($url != '' && $vhost != '' && $uuid != '') {
    $_SESSION['url'] = $url;
    $_SESSION['vhost'] = $vhost;
    $_SESSION['args'] = $args;
    $_SESSION['uuid'] = $uuid;
    $_SESSION['ip'] = $ip;
}

include "template.php";
