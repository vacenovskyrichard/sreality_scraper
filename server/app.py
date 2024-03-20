import json
from flask import Flask, jsonify, request, abort, session, Response
import os
import math
from flask import Flask, render_template, request, url_for, redirect
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from datetime import date, datetime
from datetime import datetime, timedelta, timezone
from models import db, ObjectInfo, get_uuid, EventType, ObjectType
from config import ApplicationConfig
from flask_migrate import Migrate
from scraper import FlatScraper
from marshmallow import fields, validate
from enum import Enum

app = Flask(__name__)
app.config.from_object(ApplicationConfig)
db.init_app(app=app)
migrate = Migrate(app, db)

CORS(app)

ma = Marshmallow(app)


class FlatSchema(ma.Schema):
    object_type = fields.String(validate=validate.OneOf([e.value for e in ObjectType]))
    event_type = fields.String(validate=validate.OneOf([e.value for e in EventType]))
    area = fields.String()
    image = fields.String()
    object_structure = fields.String()
    price = fields.String()
    locality = fields.String()

    class Meta:
        fields = (
            "object_type",
            "event_type",
            "area",
            "image",
            "object_structure",
            "price",
            "locality",
        )


flat_schema = FlatSchema()
flats_schema = FlatSchema(many=True)


@app.route("/get_data", methods=["GET"])
def get_data():

    # delete old records from database
    db.session.query(ObjectInfo).delete()
    db.session.commit()

    fs = FlatScraper()
    scraped_list = fs.scrapy_func()

    delimiters = [" ", "\xa0"]
    n_of_records = len(scraped_list)
    i = 1
    for item in scraped_list:
        for delimiter in delimiters:
            name = " ".join(item.name.split(delimiter))
        print(f"Progress - Flat: {i}/{n_of_records}")
        i += 1
        event_type, object_type, object_structure, object_area, m2 = name.split()[:5]

        db.session.add(
            ObjectInfo(
                object_type=ObjectType.FLAT,
                event_type=EventType.SELL,
                area=f"{object_area} {m2}",
                image=item.images[0],
                object_structure=object_structure,
                price=item.price,
                locality=item.locality,
            )
        )
    db.session.commit()

    all_records = ObjectInfo.query.all()
    results = flats_schema.dump(all_records)

    return jsonify(results), 200


if __name__ == "__main__":

    app.run(host="0.0.0.0", port=5000)
