from django.db import models
from django.contrib.auth.models  import User
from django.utils import timezone

import uuid


class BaseModel(models.Model):
    uid = models.UUIDField(default=uuid.uuid4 , editable=False , primary_key=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    
    class Meta:
        abstract = True


class Hotel(BaseModel):
    hotel_name = models.CharField(max_length=100)
    hotel_price =  models.IntegerField()
    descr=models.TextField()
    room_count = models.IntegerField(default=10)
    
    class Meta:
        ordering=['hotel_price']
    
    
    def __str__(self) -> str:
        return f"{self.hotel_name} Room"
    
    
class Hotel_room(BaseModel):
    room_type=models.ForeignKey(Hotel,related_name="room_numbers",on_delete=models.CASCADE)
    room_no=models.IntegerField(default=111)
    
    class Meta:
        ordering=['room_type']
        
    def __str__(self) -> str:
        return f"{self.room_type.hotel_name} {self.room_no}"
    
    
    

class Amenities(BaseModel):
    hotel = models.ForeignKey(Hotel, related_name="hotel_amenities" , on_delete=models.CASCADE) # hotel.images.all() // this wil return all the images of that particular hotel
    c_bed_room=models.IntegerField(default=1)
    c_bath_room=models.IntegerField(default=1)
    rating =models.IntegerField(default=5)
    has_free_wifi = models.BooleanField(default=False)
    has_ac=models.BooleanField(default=False)
    has_swimming_pool = models.BooleanField(default=False)
    has_gym = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return f"Amenities for {self.hotel.hotel_name} Room"



    
class HotelImages(BaseModel):
    hotel = models.ForeignKey(Hotel, related_name="hotel_images" , on_delete=models.CASCADE) # hotel.images.all() // this wil return all the images of that particular hotel
    images = models.ImageField(upload_to="static/hotel")
    
    def __str__(self) -> str:
        return f"Images of {self.hotel.hotel_name} Room"
    



class Services(BaseModel):
    service_name=models.CharField(max_length=50)
    service_desc=models.TextField(max_length=100,null=True,blank=True)
    service_Price=models.IntegerField(default=200)



    def __str__(self) -> str:
        return f"{self.service_name}"
    

class HotelBooking(BaseModel):
    hotel = models.ForeignKey(Hotel,related_name="hotel_booking",on_delete=models.CASCADE)
    room_nu=models.ForeignKey(Hotel_room,related_name="room_booking",on_delete=models.CASCADE)
    name = models.CharField(max_length=20,default="abc")
    user = models.ForeignKey(User, related_name="user_booking" , on_delete=models.CASCADE)
    email_ac = models.EmailField(default="abc@gmail.com")
    start_date = models.DateField()
    end_date = models.DateField()
    adult_count = models.IntegerField(default=1)
    child_count = models.IntegerField(default=0)
    special_request =models.TextField(max_length=300,default="")
    booking_date=models.DateField(auto_now_add=True,null=True)
    booking_type = models.CharField(max_length=100, choices=(('pre','Pre Paid'),('pos','Post Paid')))

    def __str__(self) -> str:
        return f"{self.hotel.hotel_name} room booked from {self.start_date} to {self.end_date}"
    
    
class Service_bookings(BaseModel):
    hotel_booking=models.ForeignKey(HotelBooking,related_name="service_booking",on_delete=models.CASCADE,null=True)
    service=models.ForeignKey(Services,related_name="booking",on_delete=models.CASCADE)
    person_count=models.IntegerField(default=2)
    deli_date=models.DateField(null=True)
    
    def __str__(self) -> str:
        return f"{self.service.service_name} booked for {self.hotel_booking}"
    
    



class Bill(BaseModel):
    booking=models.ForeignKey(HotelBooking,related_name="hotel_booking",on_delete=models.CASCADE,null=True)
    Service_charges=models.IntegerField(default=1000)
    Rent_charges=models.IntegerField(default=1000)
    Total_charges=models.IntegerField(default=2000)
    isPaid=models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"Bill for {self.booking.hotel }"
    
    
    
    
    




     
     