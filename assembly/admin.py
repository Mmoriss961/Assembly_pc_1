from django.utils.safestring import mark_safe
from .models import *
from django.contrib import admin

class AnswerInline(admin.TabularInline):
    model = Answer
class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]

class VideocardAdmin (admin.ModelAdmin):
    list_display = ('id_manuf','name','price_rub','get_img_v')
    search_fields = ('id_manuf__name','name','price_rub')
    def get_img_v(self,obj):
        if obj.video_img:
            return mark_safe(f'<img src="{obj.video_img.url}"width="65"')
        else:
            return '-'
    get_img_v.short_description = 'Изображение'

class ProcAdmin (admin.ModelAdmin):
    list_display = ('name','price_rub','get_img_v')
    search_fields = ('name','price_rub')
    def get_img_v(self,obj):
        if obj.proc_img:
            return mark_safe(f'<img src="{obj.proc_img.url}"width="65"')
        else:
            return '-'
    get_img_v.short_description = 'Изображение'

class CasePcAdmin (admin.ModelAdmin):
    list_display = ('name','price_rub','get_img_v')
    search_fields = ('name','price_rub')
    def get_img_v(self,obj):
        if obj.case_img:
            return mark_safe(f'<img src="{obj.case_img.url}"width="65"')
        else:
            return '-'
    get_img_v.short_description = 'Изображение'

class CoolerAdmin (admin.ModelAdmin):
    list_display = ('name','price_rub','get_img_v')
    search_fields = ('name','price_rub')
    def get_img_v(self,obj):
        if obj.cooler_img:
            return mark_safe(f'<img src="{obj.cooler_img.url}"width="65"')
        else:
            return '-'
    get_img_v.short_description = 'Изображение'

class DdrAdmin (admin.ModelAdmin):
    list_display = ('name','price_rub','get_img_v')
    search_fields = ('name','price_rub')
    def get_img_v(self,obj):
        if obj.ddr_img:
            return mark_safe(f'<img src="{obj.ddr_img.url}"width="65"')
        else:
            return '-'
    get_img_v.short_description = 'Изображение'

class MotherboardAdmin (admin.ModelAdmin):
    list_display = ('name','price_rub','get_img_v')
    search_fields = ('name','price_rub')
    def get_img_v(self,obj):
        if obj.mboard_img:
            return mark_safe(f'<img src="{obj.mboard_img.url}"width="65"')
        else:
            return '-'
    get_img_v.short_description = 'Изображение'

class PowerSupplyAdmin (admin.ModelAdmin):
    list_display = ('name','price_rub','get_img_v')
    search_fields = ('name','price_rub')
    def get_img_v(self,obj):
        if obj.power_supply_img:
            return mark_safe(f'<img src="{obj.power_supply_img.url}"width="65"')
        else:
            return '-'
    get_img_v.short_description = 'Изображение'

class StorageAdmin (admin.ModelAdmin):
    list_display = ('name','price_rub','get_img_v')
    search_fields = ('name','price_rub')


    def get_img_v(self,obj):
        if obj.storage_img:
            return mark_safe(f'<img src="{obj.storage_img.url}"width="65"')
        else:
            return '-'
    get_img_v.short_description = 'Изображение'




admin.site.register(Answer)
admin.site.register(Test)
admin.site.register(Question, QuestionAdmin)
admin.site.register(CasePc,CasePcAdmin)
admin.site.register(PcAssembly)
admin.site.register(Processor,ProcAdmin)
admin.site.register(Cooler,CoolerAdmin)
admin.site.register(Videocard,VideocardAdmin)
admin.site.register(Storage,StorageAdmin)
admin.site.register(Motherboard,MotherboardAdmin)
admin.site.register(PowerSupply,PowerSupplyAdmin)
admin.site.register(Result)
admin.site.register(Ddr,DdrAdmin)
admin.site.register(Manufacturer)
admin.site.register(TypeMemory)
admin.site.register(Storage_form_factor)
admin.site.register(Storage_type)
admin.site.register(Socket)

admin.site.register(Mboard_size)
admin.site.register(Feedback)

# Register your models here.

admin.site.site_title = 'Управление сайтом'
admin.site.site_header = 'Управление сайтом'
