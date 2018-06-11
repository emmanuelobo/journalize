from django.contrib import admin
from journal.models import Journal
from userprofile.models import Profile

admin.site.register(Journal)
admin.site.register(Profile)
