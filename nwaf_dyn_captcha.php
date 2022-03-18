<?php

function unblockIP($unblock_ip, $mgmt_url, $token, $proxy)
{
    $json_build = ["token" => $token, "delete_banned_ip" => $unblock_ip];
    $unblock_data = json_encode($json_build);

    $curl = curl_init();
    curl_setopt($curl, CURLOPT_URL, $mgmt_url);
    curl_setopt($curl, CURLOPT_POST, 1);
    curl_setopt($curl, CURLOPT_TIMEOUT, 15);
    curl_setopt($curl, CURLOPT_USERAGENT, "Captcha unblock");
    if ($proxy != '') {
        curl_setopt($curl, CURLOPT_PROXY, $proxy);
    }
    curl_setopt($curl, CURLOPT_POSTFIELDS, $unblock_data);

    $curlData = curl_exec($curl);
    curl_close($curl);

    return $curlData;
}
