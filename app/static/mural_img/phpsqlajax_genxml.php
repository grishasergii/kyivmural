<?php
//I am folllowing this example https://developers.google.com/maps/articles/phpsqlajax_v3

require 'dbinfo.php';

// Start XML file, create parent node

$dom = new DOMDocument("1.0");
$node = $dom->createElement("markers");
$parnode = $dom->appendChild($node);

// Opens a connection to a MySQL server

$connection = @mysqli_connect ($host, $username, $password, $database);

if (!$connection) {
   //die('Not connected : ' . mysqli_error());

   $xmlstr = file_get_contents('murals.xml');
   if ($xmlstr == false) {
      die('Cannot read murals.xml');
   } else {
      header('Content-type: text/xml');
      echo $xmlstr;
   }

} else {
   // Set the active MySQL database

   $db_selected = mysqli_select_db($connection, $database);
   if (!$db_selected) {
     die ('Can\'t use db : ' . mysqli_error());
   }

   // Select all the rows in the markers table

   $query = "SELECT * FROM murals WHERE 1";
   $result = mysqli_query($connection, $query);
   if (!$result) {
     die('Invalid query: ' . mysql_error());
   }

   header("Content-type: text/xml");

   // Iterate through the rows, adding XML nodes for each

   while ($row = @mysqli_fetch_assoc($result)){
     // ADD TO XML DOCUMENT NODE
     $node = $dom->createElement("marker");
     $newnode = $parnode->appendChild($node);
     $newnode->setAttribute("lat", $row['lat']);
     $newnode->setAttribute("lng", $row['lng']);
     $newnode->setAttribute("description", $row['description']);
     $newnode->setAttribute("copyright", $row['copyright']);
   }
   
   $dom->save('murals.xml');
   echo $dom->saveXML();

}

?>
