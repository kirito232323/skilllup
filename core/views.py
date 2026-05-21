import json
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from .models import (
    EmployeeSkill,
    Recommendation,
    SkillGapLog,
    SkillUpUser,
)


def index(request):
    return render(request, 'index.html')


@csrf_exempt
def login_view(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)

    email = request.POST.get('email', '').strip()
    password = request.POST.get('password', '').strip()

    user = authenticate(request, username=email, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({
            'success': True,
            'user': {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'role': user.account_role,
                'job_role': user.job_role.role_name if user.job_role else '',
            }
        })

    return JsonResponse({'success': False, 'message': 'Invalid credentials'})


def logout_view(request):
    logout(request)
    return redirect('/')


def session_view(request):
    if request.user.is_authenticated:
        return JsonResponse({'authenticated': True, 'user_id': request.user.id})
    return JsonResponse({'authenticated': False})


def get_dashboard_stats(request):
    user_id = request.GET.get('user_id')
    if not user_id:
        return JsonResponse({'error': 'user_id is required'}, status=400)

    try:
        user = SkillUpUser.objects.get(pk=user_id)
    except SkillUpUser.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

    skills_count = EmployeeSkill.objects.filter(user=user).count()
    recommendations_count = Recommendation.objects.filter(user=user).count()
    gaps_count = SkillGapLog.objects.filter(user=user, gap_score__gt=0).count()

    return JsonResponse({
        'skills': skills_count,
        'recommendations': recommendations_count,
        'gaps': gaps_count,
    })


def get_recommendations(request):
    user_id = request.GET.get('user_id')
    if not user_id:
        return JsonResponse({'error': 'user_id is required'}, status=400)

    try:
        user = SkillUpUser.objects.get(pk=user_id)
    except SkillUpUser.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

    records = Recommendation.objects.filter(user=user).select_related('module')
    data = []
    for rec in records:
        data.append({
            'recommendation_id': rec.id,
            'status': rec.status,
            'title': rec.module.title,
            'description': rec.module.description,
            'duration_hours': str(rec.module.duration_hours) if rec.module.duration_hours is not None else '',
        })

    return JsonResponse(data, safe=False)


def get_skill_gaps(request):
    user_id = request.GET.get('user_id')
    if not user_id:
        return JsonResponse({'error': 'user_id is required'}, status=400)

    try:
        user = SkillUpUser.objects.get(pk=user_id)
    except SkillUpUser.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

    records = SkillGapLog.objects.filter(user=user).select_related('skill')
    gaps = [
        {
            'skill_name': rec.skill.skill_name,
            'gap_score': rec.gap_score,
            'analysis_date': rec.analysis_date.isoformat(),
        }
        for rec in records
    ]

    return JsonResponse(gaps, safe=False)


def get_trainees(request):
    trainees = SkillUpUser.objects.filter(account_role='trainee').select_related('job_role').order_by('first_name')
    data = [
        {
            'id': trainee.id,
            'first_name': trainee.first_name,
            'last_name': trainee.last_name,
            'email': trainee.email,
            'job_role': trainee.job_role.role_name if trainee.job_role else '',
            'account_role': trainee.account_role,
        }
        for trainee in trainees
    ]

    return JsonResponse({'success': True, 'count': len(data), 'trainees': data})


def get_user_skills(request):
    user_id = request.GET.get('user_id')
    if not user_id:
        return JsonResponse({'error': 'user_id is required'}, status=400)

    try:
        user = SkillUpUser.objects.get(pk=user_id)
    except SkillUpUser.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

    records = EmployeeSkill.objects.filter(user=user).select_related('skill')
    skills = [
        {
            'skill_name': rec.skill.skill_name,
            'current_proficiency_level': rec.current_proficiency_level,
        }
        for rec in records
    ]

    return JsonResponse(skills, safe=False)
