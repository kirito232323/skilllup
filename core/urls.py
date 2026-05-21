from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login.php', views.login_view, name='login'),
    path('logout.php', views.logout_view, name='logout'),
    path('session.php', views.session_view, name='session'),
    path('api/get_dashboard_stats.php', views.get_dashboard_stats, name='get_dashboard_stats'),
    path('api/get_recommendations.php', views.get_recommendations, name='get_recommendations'),
    path('api/get_skill_gaps.php', views.get_skill_gaps, name='get_skill_gaps'),
    path('api/get_trainees.php', views.get_trainees, name='get_trainees'),
    path('api/get_user_skills.php', views.get_user_skills, name='get_user_skills'),
]
