from faker import Faker

fake = Faker()

USER_DATA = [{"name": fake.name()} for _ in range(50)]
PROPERTY_DATA = [
    {"name": fake.address(), "latitude": fake.latitude(), "longitude": fake.longitude()}
    for _ in range(50)
]
