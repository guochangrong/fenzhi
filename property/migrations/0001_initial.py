# Generated by Django 2.1.2 on 2018-11-21 08:39

from django.db import migrations, models
import django.utils.timezone
import djongo.models.fields
import property.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(2, 'Enabled'), (-2, 'Disabled')], default=2, verbose_name='Status')),
                ('create_user_id', models.IntegerField(editable=False, null=True, verbose_name='Create User')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Create Time')),
                ('update_user_id', models.IntegerField(editable=False, null=True, verbose_name='Update User')),
                ('update_time', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Update Time')),
                ('intentId', models.CharField(max_length=255, null=True, verbose_name='intentId')),
                ('key', models.CharField(default='', max_length=100, verbose_name='key')),
                ('answerMethod', models.IntegerField(default=1, verbose_name='answerMothod')),
                ('answerAudio', models.CharField(max_length=255, null=True, verbose_name='answerAudio')),
                ('isDefault', models.BooleanField(default=False, verbose_name='isDefault')),
                ('answerTxt', models.CharField(default='', max_length=500, verbose_name='answerTxt')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('base', djongo.models.fields.EmbeddedModelField(model_container=property.models.Base, null=True)),
                ('headline', models.CharField(max_length=225)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(2, 'Enabled'), (-2, 'Disabled')], default=2, verbose_name='Status')),
                ('create_user_id', models.IntegerField(editable=False, null=True, verbose_name='Create User')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Create Time')),
                ('update_user_id', models.IntegerField(editable=False, null=True, verbose_name='Update User')),
                ('update_time', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Update Time')),
                ('intent', models.CharField(max_length=255, null=True, verbose_name='intent')),
                ('answerTxt', models.CharField(default='', max_length=255, verbose_name='answerTxt')),
                ('answerType', models.IntegerField(default=1, verbose_name='answerType')),
                ('answerMethod', models.IntegerField(default=1, verbose_name='answerMothod')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(2, 'Enabled'), (-2, 'Disabled')], default=2, verbose_name='Status')),
                ('intent', models.CharField(default='', max_length=225, verbose_name='intent')),
                ('tech', models.CharField(default='', max_length=20, verbose_name='tech')),
                ('userId', models.CharField(default='', max_length=20, verbose_name='userId')),
                ('questionStr', models.CharField(default='', max_length=20, verbose_name='questionStr')),
                ('answerStr', models.CharField(default='', max_length=20, verbose_name='answerStr')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Create Time')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(2, 'Enabled'), (-2, 'Disabled')], default=2, verbose_name='Status')),
                ('create_user_id', models.IntegerField(editable=False, null=True, verbose_name='Create User')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Create Time')),
                ('update_user_id', models.IntegerField(editable=False, null=True, verbose_name='Update User')),
                ('update_time', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Update Time')),
                ('user_id', models.IntegerField(null=True)),
                ('nickname', models.CharField(default='', max_length=255, verbose_name='nickname')),
                ('sex', models.IntegerField(choices=[(1, 'Male'), (2, 'Female')], default=1, verbose_name='Sex')),
                ('openId', models.CharField(default='', max_length=100)),
                ('avatar', models.ImageField(blank=True, null=True, storage=property.models.UserStorage(), upload_to='user', verbose_name='Avatar')),
                ('last_login', models.DateTimeField(null=True, verbose_name='lostLogin')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
