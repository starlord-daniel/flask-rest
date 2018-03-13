from api import api

from api.modelHelper import *

from flask import Blueprint, make_response, request, jsonify
from flask.views import MethodView

import json

simple = Blueprint('simple', __name__)
model = load_model()

@simple.route('/')
@simple.route('/hello')
def hello():
    """Renders a sample page."""
    return "Hello! Please use POST requests to do predictions on '/pred'. Read more on the Github page: <LINK>"

class PredictionRoute(MethodView):
    def post(self):
        if request.json == None:
            return make_response('Please set the Content-Type to application/json', 406)
        try:
            # process the image
            image_array = process_image(request.json['image_url'])

            # run prediction on the model
            p_label, p_acc = label_and_prob(image_array, model)

            # create the formatted output
            output = "The predicted label for the image is {p_label} with an accuracy of {p_acc:.2f}".format(
                p_label = p_label,
                p_acc = p_acc
            )

            return make_response(output, 200)
        except Exception as e:
            return make_response('An error did occur: {m}'.format(m = str(e)), 500)

pred_route =  PredictionRoute.as_view('pred_route')
api.add_url_rule(
    '/pred', view_func=pred_route, methods=['POST']
)
api.add_url_rule(
    '/predict', view_func=pred_route, methods=['POST']
)