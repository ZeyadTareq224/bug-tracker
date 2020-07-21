# Generated by Django 3.0.6 on 2020-07-15 10:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('Tracker', '0003_ticket_ticket_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='project_manager',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.ProjectManager'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='developers',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.Developer'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='submitters',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.Submitter'),
        ),
    ]
