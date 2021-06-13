# Generated by Django 3.2 on 2021-06-09 11:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('assembly', '0004_answer_answer_param_ddr'),
    ]

    operations = [
        migrations.AddField(
            model_name='pcassembly',
            name='id_ddr',
            field=models.ForeignKey(db_column='Id_ddr', default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='assembly.ddr', verbose_name='Наименование памяти'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='answer',
            name='answer_param_ddr',
            field=models.CharField(db_column='Answer_param_ddr', max_length=255, verbose_name='Необходимый объем опер. памяти'),
        ),
        migrations.AlterField(
            model_name='question',
            name='id_test',
            field=models.ForeignKey(db_column='Id_test', on_delete=django.db.models.deletion.DO_NOTHING, to='assembly.test', verbose_name='Наименование теста'),
        ),
        migrations.AlterField(
            model_name='test',
            name='test_active',
            field=models.IntegerField(db_column='Test_active', verbose_name='Активный тест'),
        ),
        migrations.AlterField(
            model_name='test',
            name='test_desc',
            field=models.CharField(db_column='Test_desc', max_length=250, verbose_name='Описание'),
        ),
    ]
