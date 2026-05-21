<?php

    include '../config/database.php';

    header('Content-Type: application/json');

    $userId = $_GET['user_id'];

    $response = [];

    $skillsSql = "
    SELECT COUNT(*) AS total_skills
    FROM Employee_Skills
    WHERE user_id = ?
    ";

    $stmt = $conn->prepare($skillsSql);

    $stmt->bind_param("i", $userId);

    $stmt->execute();

    $result = $stmt->get_result();

    $response['skills'] =
        $result->fetch_assoc()['total_skills'];

    $recommendSql = "
    SELECT COUNT(*) AS total_recommendations
    FROM Recommendations
    WHERE user_id = ?
    ";

    $stmt = $conn->prepare($recommendSql);

    $stmt->bind_param("i", $userId);

    $stmt->execute();

    $result = $stmt->get_result();

    $response['recommendations'] =
        $result->fetch_assoc()['total_recommendations'];

    $gapSql = "
    SELECT COUNT(*) AS total_gaps
    FROM Skills_Gap_Logs
    WHERE user_id = ?
    AND gap_score > 0
    ";

    $stmt = $conn->prepare($gapSql);

    $stmt->bind_param("i", $userId);

    $stmt->execute();

    $result = $stmt->get_result();

    $response['gaps'] =
        $result->fetch_assoc()['total_gaps'];

    echo json_encode($response);

?>