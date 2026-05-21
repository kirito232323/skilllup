<?php
    include '../config/database.php';

    header('Content-Type: application/json');

    $userId = $_GET['user_id'];

    $sql = "
    SELECT
        Skills_Dictionary.skill_name,
        Skills_Gap_Logs.gap_score,
        Skills_Gap_Logs.analysis_date

    FROM Skills_Gap_Logs

    JOIN Skills_Dictionary
    ON Skills_Gap_Logs.skill_id =
    Skills_Dictionary.skill_id

    WHERE Skills_Gap_Logs.user_id = ?
    ";

    $stmt = $conn->prepare($sql);

    $stmt->bind_param("i", $userId);

    $stmt->execute();

    $result = $stmt->get_result();

    $gaps = [];

    while ($row = $result->fetch_assoc()) {

        $gaps[] = $row;

    }

    echo json_encode($gaps);

?>