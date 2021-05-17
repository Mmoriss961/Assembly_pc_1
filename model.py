# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Answer(models.Model):
    id_answer = models.AutoField(db_column='Id_answer', primary_key=True)  # Field name made lowercase.
    id_question = models.ForeignKey('Question', models.DO_NOTHING, db_column='Id_question')  # Field name made lowercase.
    answer_title = models.CharField(db_column='Answer_title', max_length=255)  # Field name made lowercase.
    answer_param_proc = models.CharField(db_column='Answer_param_proc', max_length=255)  # Field name made lowercase.
    answer_param_video = models.CharField(db_column='Answer_param_video', max_length=255)  # Field name made lowercase.
    answer_img = models.CharField(db_column='Answer_img', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'answer'


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
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

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
    name = models.CharField(db_column='Name', max_length=100)  # Field name made lowercase.
    max_height_cooler = models.IntegerField(db_column='Max_height_cooler')  # Field name made lowercase.
    integrated_power_supply = models.IntegerField(db_column='Integrated_power_supply', blank=True, null=True)  # Field name made lowercase.
    max_length_video = models.IntegerField(db_column='Max_length_video')  # Field name made lowercase.
    price_rub = models.IntegerField(db_column='Price_rub')  # Field name made lowercase.
    form_factor_2_5 = models.IntegerField(db_column='Form_factor_2_5', blank=True, null=True)  # Field name made lowercase.
    form_factor_3_5 = models.IntegerField(db_column='Form_factor_3_5', blank=True, null=True)  # Field name made lowercase.
    form_factor_mboard = models.CharField(db_column='Form_factor_mboard', max_length=30)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'case_pc'


class Cooler(models.Model):
    id_cooler = models.AutoField(db_column='Id_ cooler', primary_key=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    name = models.CharField(db_column='Name', max_length=100)  # Field name made lowercase.
    cooler_height = models.IntegerField(db_column='Cooler_height')  # Field name made lowercase.
    cooler_max_tdp = models.IntegerField(db_column='Cooler_Max_TDP')  # Field name made lowercase.
    cooler_socket = models.CharField(db_column='Cooler_Socket', max_length=20)  # Field name made lowercase.
    price_rub = models.IntegerField(db_column='Price_rub')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'cooler'


class Ddr(models.Model):
    id_ddr = models.AutoField(db_column='Id_DDR', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=100)  # Field name made lowercase.
    ddr_type = models.IntegerField(db_column='DDR_type')  # Field name made lowercase.
    ddr_frenquency = models.IntegerField(db_column='DDR_frenquency')  # Field name made lowercase.
    ddr_quantity = models.IntegerField(db_column='DDR_quantity')  # Field name made lowercase.
    ddr_size = models.IntegerField(db_column='DDR_size')  # Field name made lowercase.
    ddr_rub = models.IntegerField(db_column='DDR_rub')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ddr'


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


class Hdd(models.Model):
    id_hdd = models.AutoField(db_column='Id_HDD', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=100)  # Field name made lowercase.
    hdd_volume = models.IntegerField(db_column='HDD_volume')  # Field name made lowercase.
    price_rub = models.IntegerField(db_column='Price_rub')  # Field name made lowercase.
    hdd_read_speed = models.IntegerField(db_column='HDD_read_speed')  # Field name made lowercase.
    hdd_write_speed = models.IntegerField(db_column='HDD_write_speed')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'hdd'


class Motherboard(models.Model):
    name = models.CharField(db_column='Name', max_length=100, db_collation='utf8_general_ci')  # Field name made lowercase.
    id_mboard = models.AutoField(db_column='Id_mboard', primary_key=True)  # Field name made lowercase.
    mboard_size = models.CharField(db_column='Mboard_size', max_length=30)  # Field name made lowercase.
    mboard_ddr = models.IntegerField(db_column='Mboard_DDR')  # Field name made lowercase.
    mboard_max_ddr = models.IntegerField(db_column='Mboard_max_DDR')  # Field name made lowercase.
    mboard_max_frenquency_ddr = models.IntegerField(db_column='Mboard_max_frenquency_DDR')  # Field name made lowercase.
    price_rub = models.IntegerField(db_column='Price_rub')  # Field name made lowercase.
    mboard_socket = models.CharField(db_column='Mboard_socket', max_length=20)  # Field name made lowercase.
    mboard_m2 = models.IntegerField(db_column='Mboard_M2', blank=True, null=True)  # Field name made lowercase.
    mboard_sata_iii = models.IntegerField(db_column='Mboard_Sata_III')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'motherboard'


class PcAssembly(models.Model):
    id_pc_assembly = models.AutoField(db_column='Id_Pc_assembly', primary_key=True)  # Field name made lowercase.
    id_case = models.ForeignKey(CasePc, models.DO_NOTHING, db_column='Id_case')  # Field name made lowercase.
    id_cooler = models.ForeignKey(Cooler, models.DO_NOTHING, db_column='Id_cooler')  # Field name made lowercase.
    id_ddr = models.ForeignKey(Ddr, models.DO_NOTHING, db_column='Id_DDR')  # Field name made lowercase.
    id_hdd = models.ForeignKey(Hdd, models.DO_NOTHING, db_column='Id_HDD')  # Field name made lowercase.
    id_motherboard = models.ForeignKey(Motherboard, models.DO_NOTHING, db_column='Id_Motherboard')  # Field name made lowercase.
    id_power_supply = models.ForeignKey('PowerSupply', models.DO_NOTHING, db_column='Id_power_supply')  # Field name made lowercase.
    id_proc = models.ForeignKey('Processor', models.DO_NOTHING, db_column='Id_proc')  # Field name made lowercase.
    id_ssd = models.ForeignKey('Ssd', models.DO_NOTHING, db_column='Id_SSD')  # Field name made lowercase.
    id_vga = models.ForeignKey('Videocard', models.DO_NOTHING, db_column='Id_vga')  # Field name made lowercase.
    id_user = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='Id_user')  # Field name made lowercase.
    pc_assembly_date = models.DateTimeField(db_column='Pc_assembly_date')  # Field name made lowercase.
    pc_assembly_price_end = models.IntegerField(db_column='Pc_assembly_price_end')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'pc_assembly'


class PowerSupply(models.Model):
    id_power_supply = models.AutoField(db_column='Id_ power_supply', primary_key=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    name = models.CharField(db_column='Name', max_length=100)  # Field name made lowercase.
    power_supply_power = models.IntegerField(db_column='Power_supply_ power')  # Field name made lowercase. Field renamed to remove unsuitable characters.
    power_supply_pci_e = models.IntegerField(db_column='Power_supply_PCI-E')  # Field name made lowercase. Field renamed to remove unsuitable characters.
    price_rub = models.IntegerField(db_column='Price_rub')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'power_supply'


class Processor(models.Model):
    id_proc = models.AutoField(db_column='Id_proc', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=100)  # Field name made lowercase.
    socket = models.CharField(db_column='Socket', max_length=12)  # Field name made lowercase.
    number_cores = models.IntegerField(db_column='Number_cores')  # Field name made lowercase.
    proc_frequency = models.IntegerField(db_column='Proc_Frequency')  # Field name made lowercase.
    price_rub = models.IntegerField(db_column='Price_rub')  # Field name made lowercase.
    tdp = models.IntegerField(db_column='TDP')  # Field name made lowercase.
    proc_benchmark = models.IntegerField(db_column='Proc_benchmark')  # Field name made lowercase.
    proc_max_frenquency_ddr = models.IntegerField(db_column='Proc_max_frenquency_DDR')  # Field name made lowercase.
    proc_ddr = models.IntegerField(db_column='Proc_DDR')  # Field name made lowercase.
    proc_max_syze_ddr = models.IntegerField(db_column='Proc_max_syze_DDR')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'processor'


class Question(models.Model):
    id_question = models.AutoField(db_column='Id_question', primary_key=True)  # Field name made lowercase.
    id_test = models.ForeignKey('Test', models.DO_NOTHING, db_column='Id_test')  # Field name made lowercase.
    question_title = models.CharField(db_column='Question_title', max_length=255)  # Field name made lowercase.
    question_type = models.IntegerField(db_column='Question_type')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'question'


class Result(models.Model):
    id_result = models.AutoField(db_column='Id_result', primary_key=True)  # Field name made lowercase.
    result_date = models.DateTimeField(db_column='Result_date')  # Field name made lowercase.
    result_title = models.CharField(db_column='Result_title', max_length=255)  # Field name made lowercase.
    power_supply = models.CharField(db_column='Power_supply', max_length=255)  # Field name made lowercase.
    hdd = models.CharField(db_column='HDD', max_length=255)  # Field name made lowercase.
    mboard = models.CharField(db_column='Mboard', max_length=255)  # Field name made lowercase.
    proc = models.CharField(db_column='Proc', max_length=255)  # Field name made lowercase.
    id_pc_assembly = models.ForeignKey(PcAssembly, models.DO_NOTHING, db_column='Id_Pc_assembly')  # Field name made lowercase.
    video = models.CharField(db_column='Video', max_length=255)  # Field name made lowercase.
    ddr = models.CharField(db_column='DDR', max_length=255)  # Field name made lowercase.
    cooler = models.CharField(db_column='Cooler', max_length=255)  # Field name made lowercase.
    ssd = models.CharField(db_column='SSD', max_length=255)  # Field name made lowercase.
    case_pc = models.CharField(db_column='Case_pc', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'result'


class Ssd(models.Model):
    id_ssd = models.AutoField(db_column='Id_SSD', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=100)  # Field name made lowercase.
    form_factor = models.CharField(db_column='Form_factor', max_length=12)  # Field name made lowercase.
    price_rub = models.IntegerField(db_column='Price_rub')  # Field name made lowercase.
    ssd_connection_interface = models.IntegerField(db_column='SSD_connection_interface')  # Field name made lowercase.
    ssd_read_speed = models.IntegerField(db_column='SSD_read_speed')  # Field name made lowercase.
    ssd_write_speed = models.IntegerField(db_column='SSD_write_speed')  # Field name made lowercase.
    ssd_volume = models.IntegerField(db_column='SSD_volume')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ssd'


class Test(models.Model):
    id_test = models.AutoField(db_column='Id_test', primary_key=True)  # Field name made lowercase.
    test_title = models.CharField(db_column='Test_title', max_length=250)  # Field name made lowercase.
    test_desc = models.CharField(db_column='Test_desc', max_length=250)  # Field name made lowercase.
    test_active = models.IntegerField(db_column='Test_active')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'test'


class Videocard(models.Model):
    id_vga = models.AutoField(db_column='Id_vga', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=100)  # Field name made lowercase.
    video_frequency = models.IntegerField(db_column='Video_frequency')  # Field name made lowercase.
    memory_type = models.IntegerField(db_column='Memory_type')  # Field name made lowercase.
    memory_frequency = models.IntegerField(db_column='Memory_frequency')  # Field name made lowercase.
    video_memory = models.IntegerField(db_column='Video_memory')  # Field name made lowercase.
    video_benchmark = models.IntegerField(db_column='Video_benchmark')  # Field name made lowercase.
    power_supply_unit = models.IntegerField(db_column='Power_supply_unit')  # Field name made lowercase.
    video_length = models.IntegerField(db_column='Video_length')  # Field name made lowercase.
    price_rub = models.IntegerField(db_column='Price_rub')  # Field name made lowercase.
    video_pci_e = models.IntegerField(db_column='Video_PCI_e')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'videocard'
