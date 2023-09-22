# Generated by Django 4.2.5 on 2023-09-14 12:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0002_note_content'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='note',
            name='tag',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='notes.tag'),
            preserve_default=False,
        ),
    ]
