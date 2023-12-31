# Generated by Django 3.0.5 on 2023-08-29 04:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import djongo.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name_plural': 'Categorias',
            },
        ),
        migrations.CreateModel(
            name='CategoryType',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name_plural': 'Tipo de Categoria',
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name_plural': 'Departamentos',
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name_plural': 'Ubicaciones',
            },
        ),
        migrations.CreateModel(
            name='SpecialCase',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name_plural': 'Casos',
            },
        ),
        migrations.CreateModel(
            name='Specialty',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name_plural': 'Especialidad',
            },
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name_plural': 'Estados',
            },
        ),
        migrations.CreateModel(
            name='Urgency',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name_plural': 'Niveles de Urgencia',
            },
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('deadline', models.DateField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ticket.Category')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ticket.Department')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ticket.Location')),
                ('specialCase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ticket.SpecialCase')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ticket.Status')),
                ('technician', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='technician', to=settings.AUTH_USER_MODEL)),
                ('urgency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ticket.Urgency')),
                ('username', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Tickets',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ticket.Location')),
                ('specialty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ticket.Specialty')),
                ('username', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Perfil de Usuario',
            },
        ),
        migrations.AddField(
            model_name='category',
            name='categorytype',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ticket.CategoryType'),
        ),
    ]
