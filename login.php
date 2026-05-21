<?php
    session_start();

    include 'config/database.php';

    header('Content-Type: application/json');

    $email = $_POST['email'] ?? '';
    $password = $_POST['password'] ?? '';

    $sql = "
    SELECT
        Users.*,
        Job_Roles.role_name
    FROM Users
    LEFT JOIN Job_Roles
    ON Users.job_role_id = Job_Roles.role_id
    WHERE Users.email = ?
    LIMIT 1
    ";

    $stmt = $conn->prepare($sql);

    $stmt->bind_param("s", $email);

    $stmt->execute();

    $result = $stmt->get_result();

    if ($result->num_rows > 0) {

        $user = $result->fetch_assoc();

        if (password_verify($password, $user['password_hash'])) {

            $_SESSION['user_id'] = $user['user_id'];

            echo json_encode([
                "success" => true,
                "user" => [
                    "id" => $user['user_id'],
                    "first_name" => $user['first_name'],
                    "last_name" => $user['last_name'],
                    "email" => $user['email'],
                    "role" => strtolower($user['account_role']),
                    "job_role" => $user['role_name']
                ]
            ]);

        } else {

            echo json_encode([
                "success" => false,
                "message" => "Invalid password"
            ]);

        }

    } else {

        echo json_encode([
            "success" => false,
            "message" => "User not found"
        ]);

    }

?>