from django.contrib.auth.hashers import make_password
from django.db import migrations


def create_sample_users(apps, schema_editor):
    SkillUpUser = apps.get_model('core', 'SkillUpUser')
    JobRole = apps.get_model('core', 'JobRole')

    trainee_role, _ = JobRole.objects.get_or_create(
        role_name='Trainee Role',
        defaults={'description': 'Default role assigned to trainees.'}
    )
    trainer_role, _ = JobRole.objects.get_or_create(
        role_name='Trainer Role',
        defaults={'description': 'Default role assigned to trainers.'}
    )
    admin_role, _ = JobRole.objects.get_or_create(
        role_name='Administrator Role',
        defaults={'description': 'Default role assigned to administrators.'}
    )

    users = [
        {
            'email': 'ca.delarama@email.com',
            'first_name': 'Clyde',
            'last_name': 'Dela Rama',
            'account_role': 'trainee',
            'job_role': trainee_role,
            'password': 'kP9$vB2#mX!q',
            'is_staff': False,
            'is_superuser': False,
        },
        {
            'email': 'jm.rosales@email.com',
            'first_name': 'JM',
            'last_name': 'Rosales',
            'account_role': 'trainer',
            'job_role': trainer_role,
            'password': 'tZ4*fW7&gQ#s',
            'is_staff': True,
            'is_superuser': False,
        },
        {
            'email': 'a.sicat@email.com',
            'first_name': 'Ariel',
            'last_name': 'Sicat',
            'account_role': 'admin',
            'job_role': admin_role,
            'password': 'rN2!yK9$xL*b',
            'is_staff': True,
            'is_superuser': True,
        },
    ]

    for user_data in users:
        defaults = {
            'first_name': user_data['first_name'],
            'last_name': user_data['last_name'],
            'account_role': user_data['account_role'],
            'job_role': user_data['job_role'],
            'is_staff': user_data['is_staff'],
            'is_superuser': user_data['is_superuser'],
            'is_active': True,
            'password': make_password(user_data['password']),
        }
        SkillUpUser.objects.get_or_create(email=user_data['email'], defaults=defaults)


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_sample_users),
    ]
