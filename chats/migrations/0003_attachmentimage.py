# Generated by Django 4.2.16 on 2024-10-31 16:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0002_message'),
    ]

    operations = [
        migrations.CreateModel(
            name='AttachmentImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='attachment_image')),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chats.message')),
            ],
        ),
    ]