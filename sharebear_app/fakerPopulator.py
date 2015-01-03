from django_faker import Faker

from django.contrib.auth.models import User
from sharebear_app.models import UserProfile

populator = Faker.getPopulator()

populator.addEntity(User,5)
#populator.addEntity(UserProfile,5)

insertedPks = populator.execute()