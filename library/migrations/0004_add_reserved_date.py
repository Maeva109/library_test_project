from django.db import migrations, models
from django.utils import timezone

def forwards_func(apps, schema_editor):
    Reservation = apps.get_model("library", "Reservation")
    for reservation in Reservation.objects.all():
        reservation.reserved_date = timezone.now()
        reservation.save()

class Migration(migrations.Migration):
    dependencies = [
        ('library', '0003_alter_member_options_remove_member_email_and_more'),  # Use your actual previous migration filename, without .py
    ]
    
    operations = [
        migrations.AddField(
            model_name='reservation',
            name='reserved_date',
            field=models.DateTimeField(auto_now_add=True, default=timezone.now()),
        ),
        migrations.RunPython(forwards_func),
    ]