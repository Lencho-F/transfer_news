from django.contrib import admin
from .models import NewsItem, UserProfile, NewsSample, ContactResponse

# Register your models here.
class NewsSampleAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'image', 'timestamp')
  
class NewsItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'image', 'timestamp')

class ContactResponseAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'message', 'timestamp')

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'is_active', 'is_staff', 'timestamp')
    def save_model(self, request, obj, form, change):
        if not change:
            obj.set_password(obj.password)
        obj.save()


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(NewsItem, NewsItemAdmin)
admin.site.register(NewsSample, NewsSampleAdmin)
admin.site.register(ContactResponse, ContactResponseAdmin)
