

# Create your views here.
from django.shortcuts import render, redirect
from .models import*
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from datetime import datetime




def check_booking2(start_date, end_date, uid, room_count):
    qs1 = HotelBooking.objects.filter(  
        start_date__lt=start_date,
        end_date__gt=end_date,
        hotel__uid=uid
    )
    qs2 = HotelBooking.objects.filter(
        start_date__lt=start_date,
        end_date__lte=end_date,
        end_date__gte=start_date,
        hotel__uid=uid
    )
    qs3 = HotelBooking.objects.filter(
        start_date__gte=start_date,
        start_date__lte=end_date,
        end_date__gt=end_date,
        hotel__uid=uid
    )
    qs4 = HotelBooking.objects.filter(
        start_date__gte=start_date,
        end_date__lte=end_date,
        hotel__uid=uid
    )
    
    booked_rooms = len(qs1) + len(qs2) + len(qs3) + len(qs4)
    print("Booked Rooms:", booked_rooms)
    print("Room Count:", room_count)

    return booked_rooms < room_count
    
def check_booking(start_date,end_date,uid, room_nu):
    qs1 = HotelBooking.objects.filter(  
        start_date__lt = start_date,
        end_date__gt = end_date,
        room_nu=room_nu
        )
    qs2 = HotelBooking.objects.filter(
        start_date__lt = start_date,
        end_date__lte = end_date,
        end_date__gte=start_date,
        room_nu=room_nu
        )
    qs3 = HotelBooking.objects.filter(
        start_date__gte = start_date,
        start_date__lte = end_date,
        end_date__gt = end_date,
        room_nu=room_nu
        )
    qs4 = HotelBooking.objects.filter(
        start_date__gte = start_date,
        end_date__lte = end_date,
        room_nu=room_nu
        )

    booked_rooms=len(qs1)+len(qs2)+len(qs3)+len(qs4)
    

    return 0 if booked_rooms==1 else 1
    
@login_required(login_url="/login/")
def home(request):
    
    if request.method != 'POST':
        return render(request,'home.html')
    start_date=request.POST.get('start_date')
    end_date=request.POST.get('end_date')
    
    hotels=Hotel.objects.all()
    list_hotels=[]
    for hotel_obj in hotels:
        if check_booking2(start_date,end_date,hotel_obj.uid,hotel_obj.room_count)==1:
            list_hotels.insert(0,hotel_obj)

    context = {'hotel_obj' : list_hotels}

    return render(request,'room.html',context)

def contact(request):
    return render(request,'contact.html')


def room(request):
    
    hotel_obj=Hotel.objects.all()

    if request.method =="POST": 
        sort_by=request.POST.get('sort_by')
        if(sort_by=="price"):
            hotel_obj=hotel_obj.order_by('hotel_price')
        else:
            hotel_obj=hotel_obj.order_by('-hotel_amenities__rating')
        

    page = request.GET.get('page',1)
    paginator = Paginator(hotel_obj,3)
    try:
        hotel_obj = paginator.page(page)
    except PageNotAnInteger:
        hotel_obj=paginator.page(1)
    except EmptyPage:
        hotel_obj=paginator.page(paginator.num_pages)
        
        
    context = {'hotel_obj' : hotel_obj}
    
    return render(request,'room.html',context)


def login_page(request):
    if request.method =='POST':
        
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        
        user=User.objects.filter(username=username)
        if user.exists() is False:
            messages.info(request, "User do not exits. Register the user")
            return redirect('/login/')
        else:
            user=authenticate(username=username,password=password)
            if user is None:
                messages.info(request, "Invalid Password.")
                return redirect('/login/')
            else:
                login(request,user)
                return redirect('/')
                
    return render(request,"login.html")


def register(request):
    if request.method=='POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        
        user_obj=User.objects.filter(username=username)
        
        if user_obj.exists():
            messages.info(request,"This user already exists")
            return redirect('/register/')
        
        else:
            user=User.objects.create(username=username,email=email)
            user.set_password(password)
            user.save()
            return redirect('/')
    
    return render(request,"signup.html")


@login_required(login_url="/login/")
def logout_page(request):
    logout(request)
    return redirect('/login/')


@login_required
def book_hotel(request,uid):
    
    hotel_obj=Hotel.objects.get(uid = uid)

    if request.method =="POST":
        
        user=User.objects.get(username=request.user.username)
        name=request.POST.get('name')
        email_ac=request.POST.get('email')
        hotel_obj=hotel_obj
        start_date=request.POST.get('start_date')
        end_date=request.POST.get('end_date')
        adult_count=request.POST.get('adult_count')
        child_count=request.POST.get('child_count')
        special_request=request.POST.get('special_request')
        booking_type=request.POST.get('booking_type')
        
        room_nu = next(
            (
                room_num
                for room_num in hotel_obj.room_numbers.all()
                if (check_booking(start_date, end_date, uid, room_num))
            ),
            0,
        )
        
        if(room_nu!=0):
            HotelBooking.objects.create(user=user,name=name,email_ac=email_ac,hotel=hotel_obj,room_nu=room_nu,start_date=start_date,end_date=end_date,adult_count=adult_count,child_count=child_count,special_request=special_request,booking_type=booking_type)
            return render(request , 'thanku.html')
        else :
            return render(request , 'sorry.html')


    queryset = Hotel.objects.get(uid=uid)
    context = {'hotel_obj':queryset}
    return render(request , 'booking.html',context)

@login_required
def book_and_pay(request):

    print("helllo")

    return redirect('/login/')



@login_required(login_url="/login/")
def my_bookings(request):
    user=User.objects.get(username=request.user.username)
    bookings=HotelBooking.objects.filter(user=user)
    
    context = {'bookings':bookings}
    return render(request,'my_bookings.html',context)



def about(request):
    context = {'count_of_cus':len(HotelBooking.objects.all())}
    
    return render(request,'about.html',context)

@login_required(login_url="/login/")
def service(request):
    
    queryset=Services.objects.all()
    context = {'services' : queryset}
    
    return render(request,'service.html',context)


def book_service(request,uid):  # sourcery skip: extract-method
    
    user=User.objects.get(username=request.user.username)
    bookings=HotelBooking.objects.filter(user=user)
    queryset =Services.objects.get(uid = uid)

    if request.method =="POST":
        
        user=User.objects.get(username=request.user.username)
        hotel_booking_uid=request.POST.get('hotel_booking')
        hotel_booking=HotelBooking.objects.filter(uid=hotel_booking_uid)[0]
        service=queryset
        deli_date=request.POST.get('deli_date')
        person_count=request.POST.get('person_count')
        Service_bookings.objects.create(hotel_booking=hotel_booking,deli_date=deli_date,person_count=person_count,service=service)
        
        return render(request , 'thanku_ser.html')
        
    context = {'service_obj':queryset,'hotel_bookings':bookings}
    return render(request , 'service_bookings.html',context)



def generate_bill(request,uid):  # sourcery skip: extract-method, sum-comprehension
    
    booking=HotelBooking.objects.get(uid=uid) 
    bills=Bill.objects.filter(booking=booking)
    if(bills.exists()==0):
        nights_stayed = (booking.end_date - booking.start_date).days + 1
        Rent_charges=booking.hotel.hotel_price*nights_stayed
        Service_charges=0
        for services in booking.service_booking.all():
            Service_charges+=services.service.service_Price*services.person_count
        
        Total_charges=Rent_charges+Service_charges
        
        isPaid=False
        
        Bill.objects.create(booking=booking,Rent_charges=Rent_charges,Service_charges=Service_charges,isPaid=isPaid,Total_charges=Total_charges)
    
    bills=Bill.objects.filter(booking=booking)[0]
    nights_stayed = (booking.end_date - booking.start_date).days + 1
    user=booking.user
    services=booking.service_booking.all
    
    context={'bill':bills,'user':user,'hotel_booking':booking,'services':services,'nights_stayed':nights_stayed}
    return render (request,'bills.html',context)

        
    