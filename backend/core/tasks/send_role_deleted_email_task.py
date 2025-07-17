from configs.celery import app
from core.services.email_service import EmailService


@app.task
def send_role_deleted_email_task(email, name, auto_salon_name, role):
    EmailService.send_email(
        to=email,
        template_name='role_deleted.html',
        context={
            'name': name,
            'auto_salon_name': auto_salon_name,
            'role': role,
        },
        subject='Role Deleted From Auto Salon',
    )