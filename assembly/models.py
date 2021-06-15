from datetime import datetime

from django.db import models
from django.urls import reverse_lazy




class Answer(models.Model):
    id_answer = models.AutoField(db_column='Id_answer', primary_key=True)  # Field name made lowercase.
    id_question = models.ForeignKey('Question', models.DO_NOTHING,default=0, db_column='Id_question',verbose_name='Вопрос')  # Field name made lowercase.
    answer_title = models.CharField(db_column='Answer_title', max_length=255,verbose_name='Ответ')  # Field name made lowercase.
    answer_param_proc = models.CharField(db_column='Answer_param_proc', max_length=255,verbose_name='Параметр процессора')  # Field name made lowercase.
    answer_param_video = models.CharField(db_column='Answer_param_video', max_length=255, verbose_name='Параметр видеокарты')
    answer_param_ddr = models.CharField(db_column='Answer_param_ddr', max_length=255, verbose_name='Необходимый объем опер. памяти')# Field name made lowercase.
    answer_img = models.ImageField(db_column='Answer_img', max_length=255, verbose_name='Изображение', upload_to='answer/')

    def __str__(self):
        return self.answer_title

    class Meta:
        managed = True
        db_table = 'answer'
        verbose_name = 'ответ'
        verbose_name_plural = 'ответы'




class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150,verbose_name='Логин')
    first_name = models.CharField(max_length=150,verbose_name='Имя')
    last_name = models.CharField(max_length=150,verbose_name='Фамилия')
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)
    class Meta:
        managed = False
        db_table = 'auth_user'



class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class CasePc(models.Model):
    id_case = models.AutoField(db_column='Id_case', primary_key=True)  # Field name made lowercase.
    id_manuf = models.ForeignKey('Manufacturer', models.DO_NOTHING, db_column='Id_manuf', verbose_name="Производитель")
    name = models.CharField(db_column='Name', max_length=100, verbose_name='Наименование')  # Field name made lowercase.
    max_height_cooler = models.IntegerField(db_column='Max_height_cooler', verbose_name="Максимальная высота кулера")  # Field name made lowercase.
    integrated_power_supply = models.IntegerField(db_column='Integrated_power_supply',default="", blank=True, null=True, verbose_name="Встроенный блок питания,Вт" )  # Field name made lowercase.
    max_length_video = models.IntegerField(db_column='Max_length_video', verbose_name="Максимальная длинна видеокарты")  # Field name made lowercase.
    price_rub = models.IntegerField(db_column='Price_rub', verbose_name="Стоимость")  # Field name made lowercase.
    form_factor_2_5 = models.IntegerField(db_column='Form_factor_2_5', blank=True, null=True, verbose_name="Число внутренних отсеков 2,5")  # Field name made lowercase.
    form_factor_3_5 = models.IntegerField(db_column='Form_factor_3_5', blank=True, null=True, verbose_name="Число внутренних отсеков 3,5")  # Field name made lowercase.
    id_mboard_size = models.ForeignKey('Mboard_size', models.DO_NOTHING, db_column='Id_mboard_size',verbose_name="Размер мат. платы")   # Field name made lowercase.
    case_img = models.ImageField(db_column='Case_img', max_length=255, verbose_name='Изображение', upload_to='case/')

    def __str__(self):
        return self.name
    class Meta:
        managed = True
        db_table = 'case_pc'
        verbose_name = 'корпус'
        verbose_name_plural = 'корпуса'


class Cooler(models.Model):
    id_cooler = models.AutoField(db_column='Id_ cooler', primary_key=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    id_manuf = models.ForeignKey('Manufacturer', models.DO_NOTHING, db_column='Id_manuf',verbose_name="Производитель")
    name = models.CharField(db_column='Name', max_length=100,verbose_name="Наименование")  # Field name made lowercase.
    cooler_height = models.IntegerField(db_column='Cooler_height', verbose_name= "Высота кулера")  # Field name made lowercase.
    cooler_max_tdp = models.IntegerField(db_column='Cooler_Max_TDP', verbose_name= "Максимальная рассеиваемая мощность")  # Field name made lowercase.
    cooler_socket = models.ManyToManyField('Socket',db_column='Id_soket', related_name='Coolers')  # Field name made lowercase.
    price_rub = models.IntegerField(db_column='Price_rub',verbose_name= "Стоимость")  # Field name made lowercase.
    cooler_img = models.ImageField(db_column='Cooler_img', max_length=255, verbose_name='Изображение', upload_to='cooler/')

    def __str__(self):
        return self.name
    class Meta:
        managed = True
        db_table = 'cooler'
        verbose_name = 'кулер'
        verbose_name_plural = 'кулеры'



class Ddr(models.Model):
    id_ddr = models.AutoField(db_column='Id_DDR', primary_key=True)  # Field name made lowercase.
    id_manuf = models.ForeignKey('Manufacturer', models.DO_NOTHING, db_column='Id_manuf', verbose_name="Производитель")
    name = models.CharField(db_column='Name', max_length=100,verbose_name="Наименование")  # Field name made lowercase.
    ddr_type = models.ForeignKey('TypeMemory',models.DO_NOTHING,db_column='Id_type_mem',verbose_name="Тип памяти")  # Field name made lowercase.
    ddr_frenquency = models.IntegerField(db_column='DDR_frenquency',verbose_name="Частота памяти")  # Field name made lowercase.
    ddr_quantity = models.IntegerField(db_column='DDR_quantity',verbose_name="Модулей памяти в комплекте")  # Field name made lowercase.
    ddr_size = models.IntegerField(db_column='DDR_size',verbose_name="Объем одного модуля")  # Field name made lowercase.
    price_rub = models.IntegerField(db_column='DDR_rub',verbose_name="Стоимость")  # Field name made lowercase.
    ddr_img = models.ImageField(db_column='DDR_img', max_length=255, verbose_name='Изображение', upload_to='ddr/')
    def __str__(self):
        return self.name
    class Meta:
        managed = True
        db_table = 'ddr'
        verbose_name = 'оперативная память'
        verbose_name_plural = 'оперативная память'



class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)


    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'



class Motherboard(models.Model):
    id_mboard = models.AutoField(db_column='Id_mboard', primary_key=True)  # Field name made lowercase.
    id_manuf = models.ForeignKey('Manufacturer', models.DO_NOTHING, db_column='Id_manuf',verbose_name="Производитель")
    name = models.CharField(db_column='Name', max_length=100, db_collation='utf8_general_ci',verbose_name="Наименование")  # Field name made lowercase.
    id_mboard_size = models.ForeignKey('Mboard_size', models.DO_NOTHING, db_column='Id_mboard_size',verbose_name="Размер мат. платы")  # Field name made lowercase.
    id_mboard_type_ddr = models.ForeignKey('TypeMemory',models.DO_NOTHING, db_column='Id_type_mem', verbose_name="Поколение памяти, которая поддерживает мат. плата")  # Field name made lowercase.
    mboard_max_ddr = models.IntegerField(db_column='Mboard_max_DDR',verbose_name="Количество слотов памяти")  # Field name made lowercase.
    mboard_max_frenquency_ddr = models.IntegerField(db_column='Mboard_max_frenquency_DDR', verbose_name="Максимальная частота памяти, поддерживаемая мат. платой")  # Field name made lowercase.
    price_rub = models.IntegerField(db_column='Price_rub',verbose_name="Стоимость")  # Field name made lowercase.
    mboard_socket = models.ForeignKey('Socket',models.DO_NOTHING,db_column='Id_socket',verbose_name="Сокет")  # Field name made lowercase.
    mboard_m2 = models.IntegerField(db_column='Mboard_M2', blank=True, null=True, verbose_name="Количество слотов M2")  # Field name made lowercase.
    mboard_sata_iii = models.IntegerField(db_column='Mboard_Sata_III',verbose_name="Количество слотов Sata III")  # Field name made lowercase.
    mboard_img = models.ImageField(db_column='Mboard_img', max_length=255, verbose_name='Изображение', upload_to='mboard/')

    def __str__(self):
        return self.name
    class Meta:
        managed = True
        db_table = 'motherboard'
        verbose_name = 'материнская плата'
        verbose_name_plural = 'материнские платы'

class Mboard_size (models.Model):
    id_mboard_size = models.AutoField(db_column='Id_mboard_size', primary_key=True)
    name = models.CharField(db_column='Name', max_length=100, verbose_name="Наименование")

    def __str__(self):
        return self.name

    class Meta:
        managed = True
        db_table = 'mboard_size'
        verbose_name = 'размер мат. платы'
        verbose_name_plural = 'размеры мат. плат'


class PcAssembly(models.Model):
    id_pc_assembly = models.AutoField(db_column='Id_Pc_assembly', primary_key=True)  # Field name made lowercase.
    id_case = models.ForeignKey(CasePc, models.DO_NOTHING, db_column='Id_case',verbose_name="Наименовение корпуса")  # Field name made lowercase.
    id_cooler = models.ForeignKey(Cooler, models.DO_NOTHING, db_column='Id_cooler',verbose_name="Наименовение кулера")  # Field name made lowercase.
    id_storage = models.ManyToManyField('Storage', db_column='Id_storage',related_name="PcAssemblyies", verbose_name= "Наименование накопителя")  # Field name made lowercase.
    id_motherboard = models.ForeignKey(Motherboard, models.DO_NOTHING, db_column='Id_Motherboard', verbose_name="Наименование мат. платы")  # Field name made lowercase.
    id_power_supply = models.ForeignKey('PowerSupply', models.DO_NOTHING, db_column='Id_power_supply', verbose_name= "Наименование блока питания")  # Field name made lowercase.
    id_proc = models.ForeignKey('Processor', models.DO_NOTHING, db_column='Id_proc', verbose_name= "Наименование процессора")  # Field name made lowercase.
    id_vga = models.ForeignKey('Videocard', models.DO_NOTHING, db_column='Id_vga', verbose_name= "Наименование видеокарты")
    id_ddr = models.ForeignKey('Ddr', models.DO_NOTHING, db_column='Id_ddr', verbose_name= "Наименование оперативной памяти")# Field name made lowercase.
    id_user = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='Id_user', verbose_name="ФИО пользователя")  # Field name made lowercase.
    pc_assembly_date = models.DateTimeField(db_column='Pc_assembly_date', verbose_name= "Дата/время создания")  # Field name made lowercase.
    pc_assembly_price_end = models.IntegerField(db_column='Pc_assembly_price_end', verbose_name= "Итоговая цена")  # Field name made lowercase.

    def __str__(self):
        return "{} {}".format(self.id_proc, self.id_vga)


    def get_absolute_url(self):
        return reverse_lazy('detail_pc_assembly', kwargs={"id_pc_assembly": self.pk})

    class Meta:
        managed = True
        db_table = 'pc_assembly'
        verbose_name = 'сборка'
        verbose_name_plural = 'сборки'


class PowerSupply(models.Model):
    id_power_supply = models.AutoField(db_column='Id_ power_supply', primary_key=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    id_manuf = models.ForeignKey('Manufacturer', models.DO_NOTHING, db_column='Id_manuf',verbose_name='Производитель')
    name = models.CharField(db_column='Name', max_length=100,verbose_name="Наименование")  # Field name made lowercase.
    power_supply_power = models.IntegerField(db_column='Power_supply_ power',verbose_name='Мощность')  # Field name made lowercase. Field renamed to remove unsuitable characters.
    power_supply_pci_e = models.IntegerField(db_column='Power_supply_PCI-E', verbose_name="Количество разъемов 6+2-pin PCI-E")  # Field name made lowercase. Field renamed to remove unsuitable characters.
    price_rub = models.IntegerField(db_column='Price_rub',verbose_name="Стоимость")  # Field name made lowercase.
    power_supply_img = models.ImageField(db_column='Power_supply_img', max_length=255, verbose_name='Изображение', upload_to='power_supply/')

    def __str__(self):
        return self.name
    class Meta:
        managed = True
        db_table = 'power_supply'
        verbose_name = 'блок питания'
        verbose_name_plural = 'блоки питания'


class Processor(models.Model):
    id_proc = models.AutoField(db_column='Id_proc', primary_key=True)  # Field name made lowercase.
    id_manuf = models.ForeignKey('Manufacturer', models.DO_NOTHING, db_column='Id_manuf',verbose_name='Производитель')
    name = models.CharField(db_column='Name', max_length=100,verbose_name="Наименование")  # Field name made lowercase.
    id_socket = models.ForeignKey('Socket', models.DO_NOTHING, db_column='Id_socket' ,verbose_name="Сокет")  # Field name made lowercase.
    number_cores = models.IntegerField(db_column='Number_cores',verbose_name="Количество ядер")  # Field name made lowercase.
    proc_frequency = models.IntegerField(db_column='Proc_Frequency',verbose_name="Частота процессора")  # Field name made lowercase.
    price_rub = models.IntegerField(db_column='Price_rub',verbose_name="Стоимость")  # Field name made lowercase.
    tdp = models.IntegerField(db_column='TDP',verbose_name="Тепловыделение(TDP)")  # Field name made lowercase.
    proc_benchmark = models.IntegerField(db_column='Proc_benchmark',verbose_name="Число баллов в тестах")  # Field name made lowercase.
    proc_max_frenquency_ddr = models.IntegerField(db_column='Proc_max_frenquency_DDR',verbose_name="Максимальная частота опер. памяти, поддерживаемая процессором")  # Field name made lowercase.
    id_type_mem_ddr = models.ForeignKey('TypeMemory', models.DO_NOTHING, db_column='Id_type_mem', verbose_name="Тип опер. памяти, поддерживаемая процессором")  # Field name made lowercase.
    proc_max_syze_ddr = models.IntegerField(db_column='Proc_max_syze_DDR',verbose_name="Максимальный объем опер. памяти, поддерживаемый процессором")  # Field name made lowercase.
    proc_img = models.ImageField(db_column='Proc_img', max_length=255, verbose_name='Изображение', upload_to ='proc/')

    def get_absolute_url(self):
        return reverse_lazy('characteristic_proc', kwargs={"id_proc": self.pk})

    def __str__(self):
        return self.name
    class Meta:
        managed = True
        db_table = 'processor'
        verbose_name = 'процессор'
        verbose_name_plural = 'процессоры'

class Socket (models.Model):
    id_socket = models.AutoField(db_column='Id_socket', primary_key=True)
    name = models.CharField(db_column='Name', max_length=100, verbose_name="Сокет")
    def __str__(self):
        return self.name
    class Meta:
        managed = True
        db_table = 'socket'
        verbose_name = 'сокет'
        verbose_name_plural = 'сокеты'

class TypeMemory (models.Model):
    id_type_mem = models.AutoField(db_column='Id_type_mem', primary_key=True)
    name = models.CharField(db_column='Name', max_length=100,verbose_name="Тип памяти")
    def __str__(self):
        return self.name
    class Meta:
        managed = True
        db_table = 'typeMemory'
        verbose_name = 'тип памяти'
        verbose_name_plural = 'типы памяти'



class Question(models.Model):
    id_question = models.AutoField(db_column='Id_question', primary_key=True)  # Field name made lowercase.
    id_test = models.ForeignKey('Test', models.DO_NOTHING, db_column='Id_test', verbose_name="Наименование теста")  # Field name made lowercase.
    question_title = models.CharField(db_column='Question_title', max_length=255,verbose_name="Наименование")  # Field name made lowercase.
    question_type = models.IntegerField(db_column='Question_type', verbose_name="Тип вопроса")  # Field name made lowercase.

    def __str__(self):
        return self.question_title



    class Meta:
        managed = True
        db_table = 'question'
        verbose_name = 'вопрос'
        verbose_name_plural = 'вопросы'

class Test(models.Model):
    id_test = models.AutoField(db_column='Id_test', primary_key=True)  # Field name made lowercase.
    test_title = models.CharField(db_column='Test_title', max_length=250,verbose_name="Наименование")  # Field name made lowercase.
    test_desc = models.CharField(db_column='Test_desc', max_length=250, verbose_name="Описание")  # Field name made lowercase.
    test_active = models.IntegerField(db_column='Test_active', verbose_name="Активный тест")  # Field name made lowercase.

    def __str__(self):
        return self.test_title
    class Meta:
        managed = True
        db_table = 'test'
        verbose_name = 'тест'
        verbose_name_plural = 'тесты'

    def get_absolute_url(self):
        return reverse_lazy('test_view', kwargs={'id_test': self.pk})

class Result(models.Model):
    id_result = models.AutoField(db_column='Id_result', primary_key=True)  # Field name made lowercase.
    result_date = models.DateTimeField(db_column='Result_date',verbose_name="Дата/время создания")  # Field name made lowercase.
    result_title = models.CharField(db_column='Result_title', max_length=255,verbose_name="Наименование сохраненной сборки")  # Field name made lowercase.
    power_supply = models.CharField(db_column='Power_supply', max_length=255,verbose_name="Наименование блока питания")  # Field name made lowercase.
    storage = models.CharField(db_column='Storage', max_length=255,verbose_name="Наименование накопителя")  # Field name made lowercase.
    mboard = models.CharField(db_column='Mboard', max_length=255,verbose_name="Наименование мат. платы")  # Field name made lowercase.
    proc = models.CharField(db_column='Proc', max_length=255,verbose_name="Наименование процессора")  # Field name made lowercase.
    id_pc_assembly = models.ForeignKey(PcAssembly, models.DO_NOTHING, db_column='Id_Pc_assembly',verbose_name="Наименование сборки")  # Field name made lowercase.
    video = models.CharField(db_column='Video', max_length=255, verbose_name="Наименование видеокарты")  # Field name made lowercase.
    ddr = models.CharField(db_column='DDR', max_length=255, verbose_name="Наименование оперативной памяти")  # Field name made lowercase.
    cooler = models.CharField(db_column='Cooler', max_length=255, verbose_name="Наименовение кулера")  # Field name made lowercase.
    case = models.CharField(db_column='CasePC', max_length=255, verbose_name="Наименовение корпуса")
    result_price_end = models.IntegerField(db_column='Result_price_end',verbose_name="Итоговая цена")
    user = models.ForeignKey(AuthUser,models.DO_NOTHING, db_column='Id_user', verbose_name="ФИО пользователя")
    id_test = models.ForeignKey(Test, models.DO_NOTHING, db_column='Id_test', verbose_name="Наименование теста")

    def __str__(self):
        return self.result_title
    class Meta:
        managed = True
        db_table = 'result'
        verbose_name = 'сохраненная сборка'
        verbose_name_plural = 'сохраненные сборки'

    def get_absolute_url(self):
        return reverse_lazy('detail_result', kwargs={"id_result": self.pk})


class Storage(models.Model):
    id_storage = models.AutoField(db_column='Id_Storage', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=100, verbose_name="Наименование")  # Field name made lowercase.
    id_manuf = models.ForeignKey('Manufacturer', models.DO_NOTHING, db_column='Id_manuf',verbose_name="Производитель")
    id_storage_type = models.ForeignKey('Storage_type',models.DO_NOTHING,db_column='Id_storage_type',verbose_name="Тип накопителя")
    id_form_factor = models.ForeignKey('Storage_form_factor',models.DO_NOTHING,db_column='Id_form_factor',verbose_name= "Форм-фактор")  # Field name made lowercase.
    storage_volume = models.IntegerField(db_column='Storage_volume',verbose_name="Объем памяти")  # Field name made lowercase.
    storage_read_speed = models.IntegerField(db_column='Storage_read_speed',verbose_name="Скорость чтения")  # Field name made lowercase.
    storage_write_speed = models.IntegerField(db_column='Storage_write_speed',verbose_name="Скорость записи")  # Field name made lowercase.
    price_rub = models.IntegerField(db_column='Price_rub',verbose_name="Стоимость")  # Field name made lowercase.
    storage_img = models.ImageField(db_column='Storage_img', max_length=255, verbose_name='Изображение', upload_to='storage/')


    def __str__(self):
            return "{} {}".format(self.id_manuf, self.name)

    class Meta:
        managed = True
        db_table = 'storage'
        verbose_name = 'накопитель'
        verbose_name_plural = 'накопители'

class Storage_form_factor(models.Model):
    id_form_factor = models.AutoField(db_column='Id_form_factor', primary_key=True)
    name = models.CharField(db_column='Name', max_length=100, verbose_name="Форм-фактор накопителя")

    def __str__(self):
        return self.name

    class Meta:
        managed = True
        db_table = 'storage_form_factor'
        verbose_name = 'форм-фактор накопителя'
        verbose_name_plural = 'форм-фактор накопителей'

class Storage_type (models.Model):
    id_storage_type = models.AutoField(db_column='Id_storage_type', primary_key=True)
    name = models.CharField(db_column='Name', max_length=100, verbose_name="Тип накопителя")

    def __str__(self):
        return self.name

    class Meta:
        managed = True
        db_table = 'storage_type'
        verbose_name = 'тип накопителя'
        verbose_name_plural = 'типы накопителей'


class Videocard(models.Model):
    id_vga = models.AutoField(db_column='Id_vga', primary_key=True)  # Field name made lowercase.
    id_manuf = models.ForeignKey('Manufacturer', models.DO_NOTHING, db_column='Id_manuf',verbose_name="Производитель")
    name = models.CharField(db_column='Name', max_length=100, verbose_name="Наименование")  # Field name made lowercase.
    video_frequency = models.IntegerField(db_column='Video_frequency',verbose_name="Частота графического процессора")  # Field name made lowercase.
    id_type_mem = models.ForeignKey('TypeMemory', models.DO_NOTHING, db_column='Id_type_mem_',verbose_name="Тип видеопамяти")  # Field name made lowercase.
    memory_frequency = models.IntegerField(db_column='Memory_frequency', verbose_name="Частота видеопамяти")  # Field name made lowercase.
    video_memory = models.IntegerField(db_column='Video_memory',verbose_name="Объем видеопамяти")  # Field name made lowercase.
    video_benchmark = models.IntegerField(db_column='Video_benchmark', verbose_name="Число баллов в тестах")  # Field name made lowercase.
    power_supply_unit = models.IntegerField(db_column='Power_supply_unit', verbose_name="Рекомендуемая мощность блока питания")  # Field name made lowercase.
    video_length = models.IntegerField(db_column='Video_length', verbose_name="Длинна видеокарты")  # Field name made lowercase.
    price_rub = models.IntegerField(db_column='Price_rub', verbose_name="Стоимость")  # Field name made lowercase.
    video_pci_e = models.IntegerField(db_column='Video_PCI_e', blank=True, null=True, verbose_name="Дополнительное питание")  # Field name made lowercase.
    video_img = models.ImageField(db_column='Video_img', max_length=255, verbose_name='Изображение', upload_to='video/')

    def get_absolute_url(self):
        return reverse_lazy('characteristic_video', kwargs={"id_vga": self.pk})

    def __str__(self):
        return self.name

    class Meta:
        managed = True
        db_table = 'videocard'
        verbose_name = 'видеокарта'
        verbose_name_plural = 'видеокарты'

class Manufacturer(models.Model):
    id_manuf = models.AutoField(db_column='Id_manuf', primary_key=True)
    name = models.CharField(db_column='Name', max_length=100, verbose_name='Производитель')

    def __str__(self):
        return self.name

    class Meta:
        managed = True
        db_table = 'manufacturer'
        verbose_name = 'производитель'
        verbose_name_plural = 'производители'

class Feedback(models.Model):
    id_fb = models.AutoField(db_column='Id_fb', primary_key=True)
    from_email = models.EmailField(db_column='From_email', max_length=100, verbose_name='От кого отправлен Email')
    subject = models.CharField(db_column='Subject', max_length=100, verbose_name='Тема')
    message = models.CharField(db_column='Message', max_length=100, verbose_name='Сообщение')
    fb_date = models.DateTimeField(db_column='FB_date', verbose_name="Дата/время создания", default=datetime.now, blank=True)
    def __str__(self):
        return self.subject

    class Meta:
        managed = True
        db_table = 'feedback'
        verbose_name = 'обратная связь'
        verbose_name_plural = 'обратные связи'


from django.db import models

# Create your models here.
