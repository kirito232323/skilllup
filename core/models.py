from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class SkillUpUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class JobRole(models.Model):
    role_name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.role_name


class Skill(models.Model):
    CATEGORY_CHOICES = [
        ('Technical', 'Technical'),
        ('Soft Skill', 'Soft Skill'),
        ('Leadership', 'Leadership'),
    ]

    skill_name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.skill_name


class SkillUpUser(AbstractBaseUser, PermissionsMixin):
    ACCOUNT_ROLE_CHOICES = [
        ('trainee', 'Trainee'),
        ('trainer', 'Trainer'),
        ('admin', 'Admin'),
    ]

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    account_role = models.CharField(max_length=20, choices=ACCOUNT_ROLE_CHOICES)
    job_role = models.ForeignKey(JobRole, null=True, blank=True, on_delete=models.SET_NULL)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = SkillUpUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name} <{self.email}>'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'


class EmployeeSkill(models.Model):
    user = models.ForeignKey(SkillUpUser, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    current_proficiency_level = models.PositiveSmallIntegerField()
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'skill')

    def __str__(self):
        return f'{self.user.email} - {self.skill.skill_name}'


class OrganizationalStandard(models.Model):
    role = models.ForeignKey(JobRole, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    required_proficiency_level = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ('role', 'skill')

    def __str__(self):
        return f'{self.role} requires {self.skill} level {self.required_proficiency_level}'


class SkillGapLog(models.Model):
    user = models.ForeignKey(SkillUpUser, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    gap_score = models.IntegerField()
    analysis_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.email} gap {self.skill.skill_name}: {self.gap_score}'


class TrainingModule(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    target_skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    duration_hours = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Recommendation(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]

    user = models.ForeignKey(SkillUpUser, on_delete=models.CASCADE)
    module = models.ForeignKey(TrainingModule, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    date_recommended = models.DateTimeField(auto_now_add=True)
    completion_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.user.email} recommendation {self.module.title}'


class EvaluationForm(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(SkillUpUser, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class EvaluationQuestion(models.Model):
    QUESTION_TYPE_CHOICES = [
        ('multiple_choice', 'Multiple Choice'),
        ('short_answer', 'Short Answer'),
        ('rating_scale', 'Rating Scale'),
    ]

    form = models.ForeignKey(EvaluationForm, on_delete=models.CASCADE)
    question_text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPE_CHOICES)

    def __str__(self):
        return f'{self.form.title} - {self.question_text[:50]}'


class EvaluationSubmission(models.Model):
    form = models.ForeignKey(EvaluationForm, on_delete=models.CASCADE)
    user = models.ForeignKey(SkillUpUser, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.email} submission for {self.form.title}'


class EvaluationAnswer(models.Model):
    submission = models.ForeignKey(EvaluationSubmission, on_delete=models.CASCADE)
    question = models.ForeignKey(EvaluationQuestion, on_delete=models.CASCADE)
    answer_text = models.TextField(blank=True)

    def __str__(self):
        return f'Answer to {self.question.question_text[:45]}'
