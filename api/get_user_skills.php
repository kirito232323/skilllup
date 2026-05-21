<?php
    include '../config/database.php';

    $userId = $_GET['user_id'];

    $sql = "
    SELECT
        Skills_Dictionary.skill_name,
        Employee_Skills.current_proficiency_level
    FROM Employee_Skills
    JOIN Skills_Dictionary
    ON Employee_Skills.skill_id =
    Skills_Dictionary.skill_id
    WHERE Employee_Skills.user_id = ?
    ";

    $stmt = $conn->prepare($sql);

    $stmt->bind_param("i", $userId);

    $stmt->execute();

    $result = $stmt->get_result();

    $skills = [];

    while($row = $result->fetch_assoc()) {
        $skills[] = $row;
    }

    echo json_encode($skills);

?>