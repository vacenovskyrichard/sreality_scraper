from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4
from enum import Enum

db = SQLAlchemy()


def get_uuid():
    return uuid4().hex


class ObjectType(Enum):
    FLAT = "flat"
    HOUSE = "house"
    PROJECT = "project"
    LAND = "land"
    OTHER = "other"


class EventType(Enum):
    SELL = "sell"
    LEASE = "lease"
    SHARE = "share"
    AUCTION = "auction"


class ObjectInfo(db.Model):
    __tablename__ = "object_info"
    id = db.Column(db.String(32), primary_key=True, unique=True, default=get_uuid)
    object_type = db.Column(db.Enum(ObjectType), nullable=False)
    event_type = db.Column(db.Enum(EventType), nullable=False)
    area = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(150))
    object_structure = db.Column(db.String(50))
    price = db.Column(db.String(50))
    locality = db.Column(db.String(150))
