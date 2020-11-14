from flask import Flask
from flask_restful import Api

from generator.controllers.base.urls import url_patterns as base_urls
from generator.controllers.unique_id.urls import url_patterns as unique_id_urls


app = Flask(__name__)
app.url_map.strict_slashes = False
api = Api(app, prefix='')

for controller, url in base_urls:
    api.add_resource(controller, "/")

for controller, url in unique_id_urls:
    api.add_resource(controller, "/unique")
