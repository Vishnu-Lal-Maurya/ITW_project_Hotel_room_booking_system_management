from faker import Faker
fake = Faker()

import random
from .models import*

def seed_db() -> None:
    try:
        hotel_objs = Hotel.objects.all()
        for _ in range(1,4):
            for hotel_obj in hotel_objs:
                random_index =random.randint(1111, 9999)
                Hotel_room.objects.create(room_type=hotel_obj,room_no=random_index)

    except Exception as e:
        print("error")
        