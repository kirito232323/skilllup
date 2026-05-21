<?php
    include '../config/database.php';

    header('Content-Type: application/json');

    $userId = $_GET['user_id'];

    $sql = "
    SELECT
        Recommendations.recommendation_id,
        Recommendations.status,

        Training_Modules.title,
        Training_Modules.description,
        Training_Modules.duration_hours

    FROM Recommendations

    JOIN Training_Modules
    ON Recommendations.module_id =
    Training_Modules.module_id

    WHERE Recommendations.user_id = ?
    ";

    $stmt = $conn->prepare($sql);

    $stmt->bind_param("i", $userId);

    $stmt->execute();

    $result = $stmt->get_result();

    $recommendations = [];

    while ($row = $result->fetch_assoc()) {

        $recommendations[] = $row;

    }

    echo json_encode($recommendations);

?>