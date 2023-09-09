# Generated by Django 4.2.4 on 2023-09-04 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0002_carmodel_auto_park'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='carmodel',
            options={'ordering': ('id',)},
        ),
        migrations.AddField(
            model_name='carmodel',
            name='body',
            field=models.CharField(choices=[('Hatchback', 'Hatchback'), ('Sedan', 'Sedan'), ('MUV/SUV', 'Muv Suv'), ('Coupe', 'Coupe'), ('Convertible', 'Convertible'), ('Wagon', 'Wagon'), ('Van', 'Van'), ('Jeep', 'Jeep')], default='Jeep', max_length=11),
            preserve_default=False,
        ),
    ]