from flask import current_app
from flask_restplus import Resource

from ._api import *

@API.route('/version')
class About(Resource):
    def get(self):
        return {
                'api': current_app.config['VERSION'],
                'hpo': bio_phens_en.Phens.version,
                'mondo': bio_phens_en.Mondo.version,
            }

