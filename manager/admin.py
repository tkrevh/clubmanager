from django.contrib import admin
from manager.models import Organisation, Member, Aircraft, Flight, Logbook, Purpose, Document

admin.site.register(Organisation)
admin.site.register(Member)
admin.site.register(Aircraft)
admin.site.register(Logbook)
admin.site.register(Flight)
admin.site.register(Purpose)
admin.site.register(Document)
