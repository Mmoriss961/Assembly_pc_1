from django.utils.safestring import mark_safe
from .models import *
from django.contrib import admin

class VideocardAdmin (admin.ModelAdmin):
    list_display = ('name','price_rub','get_img_v')
    search_fields = ('name',)

    def get_img_v(self,obj):
        if obj.video_img:
            return mark_safe(f'<img src="{obj.video_img.url}"width="65"')
        else:
            return '-'
    get_img_v.short_description = 'Изображение'

admin.site.register(Answer)
admin.site.register(Test)
admin.site.register(Question)
admin.site.register(CasePc)
admin.site.register(PcAssembly)
admin.site.register(Processor)
admin.site.register(Cooler)
admin.site.register(Videocard,VideocardAdmin)
admin.site.register(Storage)
admin.site.register(Motherboard)
admin.site.register(PowerSupply)
admin.site.register(Result)
admin.site.register(Ddr)
admin.site.register(Manufacturer)
admin.site.register(TypeMemory)
admin.site.register(Storage_form_factor)
admin.site.register(Storage_type)
admin.site.register(Socket)
admin.site.register(Mboard_size)
admin.site.register(Feedback)

# Register your models here.
