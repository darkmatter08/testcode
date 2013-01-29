<?
$data = $_GET["data"];
echo file_get_contents("http://teamcode.co.nr/mit/http_test.php?arr=$data");
?>