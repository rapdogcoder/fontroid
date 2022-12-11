from django.contrib import admin
from .models import Images

class RecommendAdmin(admin.ModelAdmin):
    readonly_fileds= ('id','postdate',)
    pass
admin.site.register(Images, RecommendAdmin)

# Register your models here.
