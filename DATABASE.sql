CREATE DATABASE IF NOT EXISTS skillupDB;
use skillupDB;

-- 1. JOB ROLES DIRECTORY
CREATE TABLE Job_Roles (
    role_id INT PRIMARY KEY AUTO_INCREMENT,
    role_name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. SKILLS REPOSITORY
CREATE TABLE Skills_Dictionary (
    skill_id INT PRIMARY KEY AUTO_INCREMENT,
    skill_name VARCHAR(100) NOT NULL UNIQUE,
    category ENUM('Technical', 'Soft Skill', 'Leadership') NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. USERS & ACCOUNT MANAGEMENT
CREATE TABLE Users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    account_role ENUM(
        'trainee',
        'trainer',
        'admin'
    ) NOT NULL,
    job_role_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_users_job_role
        FOREIGN KEY (job_role_id)
        REFERENCES Job_Roles(role_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);

ALTER TABLE Users
MODIFY account_role ENUM(
    'trainee',
    'trainer',
    'admin'
) NOT NULL;

-- 4. EMPLOYEE SKILLS ASSESSMENT MODULE
CREATE TABLE Employee_Skills (
    emp_skill_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    skill_id INT NOT NULL,

    current_proficiency_level INT NOT NULL
        CHECK (current_proficiency_level BETWEEN 1 AND 5),

    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_emp_skills_user
        FOREIGN KEY (user_id)
        REFERENCES Users(user_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    CONSTRAINT fk_emp_skills_skill
        FOREIGN KEY (skill_id)
        REFERENCES Skills_Dictionary(skill_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    CONSTRAINT uq_employee_skill
        UNIQUE (user_id, skill_id)
);

-- 5. ORGANIZATIONAL STANDARDS MODULE
CREATE TABLE Organizational_Standards (
    standard_id INT PRIMARY KEY AUTO_INCREMENT,

    role_id INT NOT NULL,
    skill_id INT NOT NULL,

    required_proficiency_level INT NOT NULL
        CHECK (required_proficiency_level BETWEEN 1 AND 5),

    CONSTRAINT fk_orgstandards_role
        FOREIGN KEY (role_id)
        REFERENCES Job_Roles(role_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    CONSTRAINT fk_orgstandards_skill
        FOREIGN KEY (skill_id)
        REFERENCES Skills_Dictionary(skill_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    CONSTRAINT uq_role_skill_standard
        UNIQUE (role_id, skill_id)
);

-- 6. SKILLS GAP ANALYSIS MODULE
CREATE TABLE Skills_Gap_Logs (
    log_id INT PRIMARY KEY AUTO_INCREMENT,

    user_id INT NOT NULL,
    skill_id INT NOT NULL,

    gap_score INT NOT NULL,

    analysis_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_gaplogs_user
        FOREIGN KEY (user_id)
        REFERENCES Users(user_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    CONSTRAINT fk_gaplogs_skill
        FOREIGN KEY (skill_id)
        REFERENCES Skills_Dictionary(skill_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- 7. TRAINING MODULES REPOSITORY
CREATE TABLE Training_Modules (
    module_id INT PRIMARY KEY AUTO_INCREMENT,

    title VARCHAR(150) NOT NULL,
    description TEXT,

    target_skill_id INT NOT NULL,

    duration_hours DECIMAL(5,2),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_training_skill
        FOREIGN KEY (target_skill_id)
        REFERENCES Skills_Dictionary(skill_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- 8. RECOMMENDATION MODULE
CREATE TABLE Recommendations (
    recommendation_id INT PRIMARY KEY AUTO_INCREMENT,

    user_id INT NOT NULL,
    module_id INT NOT NULL,

    status ENUM(
        'Pending',
        'In Progress',
        'Completed'
    ) DEFAULT 'Pending',

    date_recommended TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    completion_date TIMESTAMP NULL,

    CONSTRAINT fk_recommend_user
        FOREIGN KEY (user_id)
        REFERENCES Users(user_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    CONSTRAINT fk_recommend_module
        FOREIGN KEY (module_id)
        REFERENCES Training_Modules(module_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- 9. EVALUATION FORMS
CREATE TABLE Evaluation_Forms (
    form_id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    created_by INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (created_by)
    REFERENCES Users(user_id)
);

CREATE TABLE Evaluation_Questions (
    question_id INT PRIMARY KEY AUTO_INCREMENT,
    form_id INT NOT NULL,
    question_text TEXT NOT NULL,
    question_type ENUM(
        'multiple_choice',
        'short_answer',
        'rating_scale'
    ) NOT NULL,

    FOREIGN KEY (form_id)
    REFERENCES Evaluation_Forms(form_id)
    ON DELETE CASCADE
);

CREATE TABLE Evaluation_Submissions (
    submission_id INT PRIMARY KEY AUTO_INCREMENT,
    form_id INT NOT NULL,
    user_id INT NOT NULL,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (form_id)
    REFERENCES Evaluation_Forms(form_id),

    FOREIGN KEY (user_id)
    REFERENCES Users(user_id)
);

CREATE TABLE Evaluation_Answers (
    answer_id INT PRIMARY KEY AUTO_INCREMENT,
    submission_id INT NOT NULL,
    question_id INT NOT NULL,
    answer_text TEXT,

    FOREIGN KEY (submission_id)
    REFERENCES Evaluation_Submissions(submission_id)
    ON DELETE CASCADE,

    FOREIGN KEY (question_id)
    REFERENCES Evaluation_Questions(question_id)
    ON DELETE CASCADE
);

-- INDEXES
CREATE INDEX idx_users_role
ON Users(job_role_id);

CREATE INDEX idx_emp_skills_user
ON Employee_Skills(user_id);

CREATE INDEX idx_emp_skills_skill
ON Employee_Skills(skill_id);

CREATE INDEX idx_orgstandards_role
ON Organizational_Standards(role_id);

CREATE INDEX idx_gaplogs_user
ON Skills_Gap_Logs(user_id);

CREATE INDEX idx_recommendations_user
ON Recommendations(user_id);

-- =========================================
-- SKILLUP SAMPLE SYSTEM DATA
-- =========================================

USE skillupDB;

-- =========================================
-- JOB ROLES
-- =========================================

INSERT INTO Job_Roles (
    role_name,
    description
)
VALUES
(
    'Frontend Developer',
    'Handles frontend web application development'
),
(
    'Training Coordinator',
    'Manages evaluations and training programs'
),
(
    'System Administrator',
    'Manages overall platform operations'
);

-- =========================================
-- SKILLS REPOSITORY
-- =========================================

INSERT INTO Skills_Dictionary (
    skill_name,
    category,
    description
)
VALUES
(
    'JavaScript',
    'Technical',
    'Frontend scripting and interactivity'
),
(
    'UI/UX Design',
    'Technical',
    'User interface and user experience design'
),
(
    'Communication',
    'Soft Skill',
    'Professional communication skills'
),
(
    'Leadership',
    'Leadership',
    'Team leadership and management'
),
(
    'Database Management',
    'Technical',
    'MySQL database administration'
),
(
    'Problem Solving',
    'Soft Skill',
    'Analytical and critical thinking skills'
);

-- =========================================
-- USERS
-- PASSWORDS:
-- trainee  -> kP9$vB2#mX!q
-- trainer  -> tZ4*fW7&gQ#s
-- admin    -> rN2!yK9$xL*b
-- =========================================

INSERT INTO Users (
    first_name,
    last_name,
    email,
    password_hash,
    account_role,
    job_role_id
)
VALUES
(
    'Clyde Andrei',
    'Delarama',
    'ca.delarama@email.com',

    '$2y$10$ej.2Bay8LcNrvLVn.GyNyucXWPcPH0T6paZD1HsGGJ9vCl2pJEy3u',

    'Trainee',
    1
),
(
    'John Michael',
    'Rosales',
    'jm.rosales@email.com',

    '$2y$10$1K1EgbLEXFCf3vtVOA5psub5/Mwcgyn9qbaXb12iIPg2MPpyPSgpi',

    'Trainer',
    2
),
(
    'Arvey',
    'Sicat',
    'a.sicat@email.com',

    '$2y$10$9MkbkXkmj62lcqRdQ1O6pOLKHd40MdAFbiQ/L5/SfKDNkoXquh6Xa',

    'Admin',
    3
);

-- =========================================
-- EMPLOYEE SKILLS
-- =========================================

INSERT INTO Employee_Skills (
    user_id,
    skill_id,
    current_proficiency_level
)
VALUES
(1, 1, 3),
(1, 2, 4),
(1, 3, 3),
(1, 6, 2),

(2, 1, 4),
(2, 3, 5),
(2, 4, 4),
(2, 6, 4),

(3, 1, 5),
(3, 4, 5),
(3, 5, 5),
(3, 6, 5);

-- =========================================
-- ORGANIZATIONAL STANDARDS
-- =========================================

INSERT INTO Organizational_Standards (
    role_id,
    skill_id,
    required_proficiency_level
)
VALUES

-- Frontend Developer
(1, 1, 5),
(1, 2, 5),
(1, 3, 4),
(1, 6, 4),

-- Training Coordinator
(2, 3, 5),
(2, 4, 5),
(2, 6, 5),

-- System Administrator
(3, 1, 5),
(3, 5, 5),
(3, 4, 5);

-- =========================================
-- TRAINING MODULES
-- =========================================

INSERT INTO Training_Modules (
    title,
    description,
    target_skill_id,
    duration_hours
)
VALUES
(
    'Advanced JavaScript Fundamentals',
    'Improve JavaScript proficiency and frontend logic',
    1,
    18
),
(
    'UI/UX Design Principles',
    'Improve interface and experience design skills',
    2,
    12
),
(
    'Professional Communication Workshop',
    'Enhance workplace communication skills',
    3,
    10
),
(
    'Leadership Essentials',
    'Develop leadership and team management skills',
    4,
    14
),
(
    'MySQL Database Administration',
    'Learn advanced database management techniques',
    5,
    16
),
(
    'Critical Thinking & Problem Solving',
    'Improve analytical and decision-making skills',
    6,
    8
);

-- =========================================
-- RECOMMENDATIONS
-- =========================================

INSERT INTO Recommendations (
    user_id,
    module_id,
    status
)
VALUES
(1, 1, 'Pending'),
(1, 6, 'In Progress'),

(2, 4, 'Pending'),
(2, 3, 'Completed'),

(3, 5, 'Completed');

-- =========================================
-- SKILLS GAP LOGS
-- =========================================

INSERT INTO Skills_Gap_Logs (
    user_id,
    skill_id,
    gap_score
)
VALUES
(1, 1, 2),
(1, 6, 2),
(2, 4, 1),
(3, 5, 0);

-- =========================================
-- EVALUATION FORMS
-- =========================================

INSERT INTO Evaluation_Forms (
    title,
    description,
    created_by
)
VALUES
(
    'Frontend Competency Assessment',
    'Evaluation for frontend development competencies',
    2
),
(
    'Leadership & Communication Assessment',
    'Evaluation for communication and leadership skills',
    2
);

-- =========================================
-- EVALUATION QUESTIONS
-- =========================================

INSERT INTO Evaluation_Questions (
    form_id,
    question_text,
    question_type
)
VALUES

-- Form 1
(
    1,
    'How confident are you in JavaScript DOM manipulation?',
    'rating_scale'
),
(
    1,
    'Explain your experience with responsive design.',
    'short_answer'
),

-- Form 2
(
    2,
    'How do you handle team conflicts?',
    'short_answer'
),
(
    2,
    'Rate your communication skills.',
    'rating_scale'
);

-- =========================================
-- SAMPLE EVALUATION SUBMISSION
-- =========================================

INSERT INTO Evaluation_Submissions (
    form_id,
    user_id
)
VALUES
(
    1,
    1
);

-- =========================================
-- SAMPLE EVALUATION ANSWERS
-- =========================================

INSERT INTO Evaluation_Answers (
    submission_id,
    question_id,
    answer_text
)
VALUES
(
    1,
    1,
    '4'
),
(
    1,
    2,
    'I have experience building responsive dashboards using HTML, CSS, and JavaScript.'
);

-- =========================================
-- END OF SAMPLE DATA
-- =========================================

SELECT first_name, password_hash FROM users;