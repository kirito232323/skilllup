<?php
    include '../config/database.php';

    header('Content-Type: application/json');

    $sql = "
    SELECT
        Users.user_id,
        Users.first_name,
        Users.last_name,
        Users.email,
        Users.account_role,
        Job_Roles.role_name

    FROM Users

    LEFT JOIN Job_Roles
    ON Users.job_role_id = Job_Roles.role_id

    WHERE LOWER(Users.account_role) = 'trainee'

    ORDER BY Users.first_name ASC
    ";

    $result = $conn->query($sql);

    if(!$result){

        echo json_encode([
            "success" => false,
            "mysql_error" => $conn->error
        ]);

        exit;

    }

    $trainees = [];

    while($row = $result->fetch_assoc()) {

        $trainees[] = [
            "id" => $row['user_id'],
            "first_name" => $row['first_name'],
            "last_name" => $row['last_name'],
            "email" => $row['email'],
            "job_role" => $row['role_name'],
            "account_role" => $row['account_role']
        ];

    }

    echo json_encode([
        "success" => true,
        "count" => count($trainees),
        "trainees" => $trainees
    ]);

?>