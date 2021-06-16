<?php
    $conn=new mysqli("remotemysql.com","RIcvQcz1ZB","98U4LQX9u7","RIcvQcz1ZB");

    if($conn){
    }
    else{
    }
 
    $image = $_POST['image'];
    $name = $_POST['name'];
    
    $img = base64_decode($image);
    $image = $name;
    file_put_contents($image, $img);
    
    $conn->query("insert into upload (image) values('email1','".$image."')");

?>
