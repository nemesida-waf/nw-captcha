<?php

require_once "Settings.php";

class DB
{
    public $LINK;
    private static $instance = null;

    private function __construct()
    {
        try {
            $dns = "sqlite:" . Settings::$DB_PATH;
            $this->LINK = new PDO($dns);
            return $this->LINK;
        } catch (PDOException $e) {

        }
    }

    public static function getInstance()
    {
        if (self::$instance === null) {
            return self::$instance = new self();
        } else return self::$instance;
    }

    public function get_para_by_db($uuid)
    {
        $query = $this->LINK->prepare("SELECT url, token FROM client WHERE waf_id=(SELECT waf_id FROM client WHERE uuid=:uuid)");
        $query->bindParam(':uuid', $uuid, PDO::PARAM_STR);
        $query->execute();
        return $query->fetchall(PDO::FETCH_ASSOC);
    }
}
