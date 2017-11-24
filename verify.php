<?php
$http_headers = getallheaders();
$http_header_keys = [];
foreach ($http_headers as $key => $value) {
    array_push($http_header_keys, strtoupper($key));
}
if (in_array("HTTP_X_FORWARDED_FOR", $http_header_keys)) {
    echo "transparent";
} elseif (in_array("HTTP_VIA", $http_header_keys)) {
    echo "anonymous";
} else {
    echo "elite";
}
