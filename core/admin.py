from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    JobRole,
    Skill,
    SkillUpUser,
    EmployeeSkill,
    OrganizationalStandard,
    SkillGapLog,
    TrainingModule,
    Recommendation,
    EvaluationForm,
    EvaluationQuestion,
    EvaluationSubmission,
    EvaluationAnswer,
)


@admin.register(SkillUpUser)
class SkillUpUserAdmin(UserAdmin):
    model = SkillUpUser
    list_display = ('email', 'first_name', 'last_name', 'account_role', 'is_staff')
    list_filter = ('account_role', 'is_staff', 'is_superuser')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'job_role', 'account_role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'account_role', 'password1', 'password2'),
        }),
    )


admin.site.register(JobRole)
admin.site.register(Skill)
admin.site.register(EmployeeSkill)
admin.site.register(OrganizationalStandard)
admin.site.register(SkillGapLog)
admin.site.register(TrainingModule)
admin.site.register(Recommendation)
admin.site.register(EvaluationForm)
admin.site.register(EvaluationQuestion)
admin.site.register(EvaluationSubmission)
admin.site.register(EvaluationAnswer)
