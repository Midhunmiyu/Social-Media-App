from faker import Faker
from user.models import CustomUser

fake = Faker()

def create_users():

    for i in range(10):
        CustomUser.objects.create_user(
            username=fake.name(),
            email=fake.email(),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            phone=fake.phone_number(),
            gender=fake.random_element(elements=('Male', 'Female')),
            dob=fake.date(),
            tc=True,
        )