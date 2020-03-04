from datetime import datetime
from faker import Faker
from random import randint, choice
from random import random
from random import choices
from random import shuffle
from app import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, nullable=False, unique=True)

    # basical info: need to transfer to device.
    username = db.Column(db.String(64), unique=True, index=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    sex = db.Column(db.SmallInteger, nullable=False)
    height = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    telephone = db.Column(db.String(35), nullable=False)

    # info stored in server.
    email = db.Column(db.String(64))
    location = db.Column(db.String(64))
    activation_time = db.Column(db.DateTime(), default=datetime.utcnow())
    last_sync = db.Column(db.DateTime(), default=datetime.utcnow)

    # health param
    locate_type = db.Column(db.SmallInteger)
    status = db.Column(db.SmallInteger, default=0)
    body_temperature = db.Column(db.Float)
    heart_rate = db.Column(db.Integer)
    blood_oxygen = db.Column(db.Float)
    # 纬度
    latitude = db.Column(db.String(30))
    # 经度
    longitude = db.Column(db.String(30))

    def __repr__(self):
        return '<User %r>' % self.username

    def grow1(self):
        self.age=self.age+1
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def insert_users():
        faker = Faker(locale=['zh_CN', 'en_US', 'zh_TW'])
        for _ in range(20):
            age_list = generate_age()
            user = User(device_id=randint(1, 100000),
                        username=name_gender(faker=faker)[0],
                        age=faker.random_element(age_list),
                        sex=name_gender(faker=faker)[1],
                        height=randint(150, 220),
                        weight=round(random() * 100 + float(20), 1),
                        telephone=faker.phone_number(),
                        email=faker.email(),
                        location=faker.address(),
                        activation_time=faker.past_datetime('-1500d'),
                        last_sync=faker.past_datetime('-365d')
                        )
            db.session.add(
               user
            )
            try:
                db.session.commit()
            except:
                db.session.rollback()

    def sync_user_data(self):
        self.locate_type = randint(0, 1)

        statusType = [0, 1, 2, 3, 4]
        statusWeight = [0.7, 0.05, 0.05, 0.1, 0.1]
        self.status = choices(statusType, statusWeight)

        # 体温，心率，血氧
        self.body_temperature = choice(generate_body_temperature())
        self.heart_rate = choice(generate_heart_rate())
        self.blood_oxygen = choice(generate_blood_oxygen())
        faker = Faker(locale=['zh_CN', 'en_US'])
        local_latlng = faker.local_latlng('CN', False)
        self.latitude = local_latlng[0]
        self.longitude = local_latlng[1]


# def test_age():
#     age_list = generate_age()
#     a = 0
#     b = 0
#     c = 0
#     d = 0
#     e = 0
#     f = 0
#     for i in age_list:
#         if i <= 10:
#             a = a + 1
#         elif i <= 25:
#             b = b + 1
#         elif i <= 30:
#             c = c + 1
#         elif i <= 50:
#             d = d + 1
#         elif i <= 70:
#             e = e + 1
#         elif i <= 111:
#             f = f + 1
#     print(len(age_list))
#     print(a / len(age_list))
#     print(b / len(age_list))
#     print(c / len(age_list))
#     print(d / len(age_list))
#     print(e / len(age_list))
#     print(f / len(age_list))
#
#
# def test_temperature():
#     temperature_list = generate_body_temperature()
#     a = 0
#     b = 0
#     c = 0
#     d = 0
#     for i in temperature_list:
#         if i <= 36.3:
#             a = a + 1
#         elif i <= 37.2:
#             b = b + 1
#         elif i <= 38.0:
#             c = c + 1
#         elif i <= 41.2:
#             d = d + 1
#     print(len(temperature_list))
#     print(a / len(temperature_list))
#     print(b / len(temperature_list))
#     print(c / len(temperature_list))
#     print(d / len(temperature_list))
#
#
# def test_heart_rate():
#     heart_list = generate_heart_rate()
#     a = 0
#     b = 0
#     c = 0
#     for i in heart_list:
#         if i <= 70:
#             a = a + 1
#         elif i <= 80:
#             b = b + 1
#         elif i <= 100:
#             c = c + 1
#     print(len(heart_list))
#     print(a / len(heart_list))
#     print(b / len(heart_list))
#     print(c / len(heart_list))
#
#
# def test_blood_oxygen():
#     blood_oxygen_list = generate_blood_oxygen()
#     a = 0
#     b = 0
#     c = 0
#     for i in blood_oxygen_list:
#         if i <= 0.95:
#             a = a + 1
#         elif i <= 0.99:
#             b = b + 1
#         elif i <= 1.00:
#             c = c + 1
#     print(len(blood_oxygen_list))
#     print(a / len(blood_oxygen_list))
#     print(b / len(blood_oxygen_list))
#     print(c / len(blood_oxygen_list))


# 不同年龄段的人数不同，(非平均分布)
def generate_age(number=1500):
    # generate 150个age, other total number maybe wrong because of num of float
    age_range = [1, 10, 25, 30, 50, 70, 111]
    weights = [0.14, 0.36, 0.16, 0.10, 0.20, 0.04]
    num_in_different_age_range = [int(i * number) for i in weights]
    age_list = []
    for i in range(len(weights)):
        for _ in range(num_in_different_age_range[i]):
            age_list.append((randint(age_range[i], age_range[i + 1])))
    shuffle(age_list)
    return age_list


def generate_body_temperature(number=1500):
    temperature_range = [35.8, 36.3, 37.2, 38.0, 41.2]
    weights = [0.02, 0.9, 0.06, 0.02]
    num_in_different_temperature_range = [int(i * number) for i in weights]
    temperature_list = []
    for i in range(len(weights)):
        for _ in range(num_in_different_temperature_range[i]):
            temperature_list.append(
                round(
                    temperature_range[i] + random() * (temperature_range[i + 1] - temperature_range[i]), 1)
            )
    shuffle(temperature_list)
    return temperature_list


def generate_heart_rate(number=1500):
    heart_rate_range = [55, 70, 80, 100]
    weights = [0.4, 0.35, 0.25]
    num_in_different_heart_rate_range = [int(i * number) for i in weights]
    heart_rate_list = []
    for i in range(len(weights)):
        for _ in range(num_in_different_heart_rate_range[i]):
            heart_rate_list.append((randint(heart_rate_range[i], heart_rate_range[i + 1])))
    shuffle(heart_rate_list)
    return heart_rate_list


def generate_blood_oxygen(number=1500):
    blood_oxygen_range = [0.94, 0.95, 0.99, 1.00]
    weights = [0.02, 0.94, 0.04]
    num_in_different_blood_oxygen_range = [int(i * number) for i in weights]
    blood_oxygen_list = []
    for i in range(len(weights)):
        for _ in range(num_in_different_blood_oxygen_range[i]):
            blood_oxygen_list.append(
                round(
                    blood_oxygen_range[i] + random() * (blood_oxygen_range[i + 1] - blood_oxygen_range[i]), 3)
            )
    shuffle(blood_oxygen_list)
    return blood_oxygen_list


def name_gender(faker):
    faker = faker
    gender = randint(0, 1)
    if gender == 0:
        name = faker.name_male()
    else:
        name = faker.name_female()
    return name, gender
