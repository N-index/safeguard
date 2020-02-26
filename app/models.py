from datetime import datetime

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
    telephone = db.Column(db.String(20), nullable=False)

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
    latitude = db.Column(db.String(30))
    longitude = db.Column(db.String(30))

    def __repr__(self):
        return '<User %r>' % self.username

    # @staticmethod
    # def insert_users():
    #     faker = Faker(['zh-CN', 'en_US'])
    #     for _ in range(100):
    #         db.session.add(
    #             User(
    #                 username=faker.name(),
    #                 email=faker.email(),
    #                 role=Role.query.filter_by(default=True).first(),
    #                 about_me=faker.sentence(10),
    #                 member_since=faker.past_datetime(start_date='-366d', tzinfo=None)
    #             )
    #         )
    #         try:
    #             db.session.commit()
    #         except:
    #             db.session.rollback()
