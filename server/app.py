import json
from flask import Flask, jsonify, request, abort, session, Response
import os
import math
from flask import Flask, render_template, request, url_for, redirect
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from datetime import date, datetime
from datetime import datetime, timedelta, timezone
from models import db, FlatToSell, get_uuid
from config import ApplicationConfig
from flask_migrate import Migrate
from scraper import FlatScraper

app = Flask(__name__)
app.config.from_object(ApplicationConfig)
db.init_app(app=app)
migrate = Migrate(app, db)

CORS(app)

ma = Marshmallow(app)


class FlatSchema(ma.Schema):
    class Meta:
        fields = (
            "object_type",
            "event_type",
            "area",
            "image",
            "object_structure",
            "price",
        )


flat_schema = FlatSchema()
flats_schema = FlatSchema(many=True)


@app.route("/get_data", methods=["GET"])
def login():

    fs = FlatScraper()
    scraped_list = fs.scrapy_func()

    result_list = []

    for item in scraped_list:
        db.session.add(FlatToSell(name=item.name, image=item.images[0]))
        db.session.commit()

    all_records = FlatToSell.query.all()
    results = flats_schema.dump(all_records)

    return jsonify(results), 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)
