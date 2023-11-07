from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(Hotel)
admin.site.register(HotelImages)
admin.site.register(Hotel_room)
admin.site.register(Amenities)
admin.site.register(HotelBooking)
admin.site.register(Service_bookings)
admin.site.register(Services)
admin.site.register(Bill)