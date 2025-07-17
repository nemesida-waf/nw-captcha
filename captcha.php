<?php

function unblockIP($unblock_ip, $url, $token, $proxy)
{

    $curl = curl_init();

    if ($proxy != '') {
        curl_setopt($curl, CURLOPT_PROXY, $proxy);
    }

    curl_setopt($curl, CURLOPT_URL, $url);
    curl_setopt($curl, CURLOPT_TIMEOUT, 15);
    curl_setopt($curl, CURLOPT_USERAGENT, "CAPTCHAv4");
    curl_setopt($curl, CURLOPT_HTTPHEADER, array(
        "x-nwaf-captcha-v4: {\"token\": $token, \"delete_banned_ip\": $unblock_ip}"
    ));
    curl_setopt($curl, CURLOPT_HEADER, false);

    $curlData = curl_exec($curl);
    curl_close($curl);

    return $curlData;
}
