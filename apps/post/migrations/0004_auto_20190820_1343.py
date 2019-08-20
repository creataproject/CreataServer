# Generated by Django 2.2 on 2019-08-20 04:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0003_post_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='cuts',
        ),
        migrations.AddField(
            model_name='cut',
            name='post',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='post.Post', verbose_name='게시물'),
        ),
    ]
