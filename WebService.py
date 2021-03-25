from flask import Flask, jsonify, request
# from mybackend import Database as backend
import FlightsManagerServer as flightsManager
import SchedulerManager

app = Flask(__name__)


@app.route('/')
def get_recommendations():
    try:
        # get the arguments from the url
        startlocation = request.args.get('startlocation', '')
        timeduration = int(request.args.get('timeduration', 0))
        k = int(request.args.get('k', 0))
        # returns the recommendations
        # return jsonify(backend().get_recommendations(startlocation, timeduration, k))
    except Exception:
        # in case one of the input is not valid return empty json
        return jsonify([])

# import binascii
# import os
#
#
# def encode_multipart_formdata(fields):
#     boundary = binascii.hexlify(os.urandom(16)).decode('ascii')
#
#     body = (
#         "".join("--%s\r\n"
#                 "Content-Disposition: form-data; name=\"%s\"\r\n"
#                 "\r\n"
#                 "%s\r\n" % (boundary, field, value)
#                 for field, value in fields.items()) +
#         "--%s--\r\n" % boundary
#     )
#
#     content_type = "multipart/form-data; boundary=%s" % boundary
#
#     return body, content_type
# from werkzeug import secure_filename


@app.route('/upload_flight', methods=['POST'])
def upload_flight():
    file = request.files['file']
    locationTags = request.form['locationTags']
    parameters = request.form['parameters'].split(",")
    values = request.form['values'].split(",")
    # file.save(secure_filename(file.filename))
    flightsManager.upload_flight(file, locationTags, parameters, values)

    # f.save(secure_filename(f.filename))
    return jsonify(data='file uploaded successfully')
    # return 'file uploaded successfully'

    # if request.is_json:
        # request_dict = request.get_json()
        # print(request_dict)
        # nickname = request_dict.get('nickname')
        # password = request_dict.get('password')
        # response = GuestRole.register(nickname, password)  # seems OK, checked
        # if response:
        #     return jsonify(msg=response['msg'], data=response['response'])
        # return jsonify(msg="Registered successfully!")
    # return jsonify(msg="Registration failed", data=response['response'], status=400)


@app.route('/get_model_parameters', methods=['GET'])
def get_model_parameters():
    if request.is_json:
        request_dict = request.get_json()
        print(request_dict)
        model_name = request_dict.get('model_name')
        response = SchedulerManager().get_model_parameters(model_name)
        if response:
            return jsonify(msg=response['msg'], data=response['response'])
    return jsonify(msg="Registered successfully!")

    # locationTags = request.form['locationTags']
    # parameters = request.form['parameters'].split(",")
    # values = request.form['values'].split(",")
    # # file.save(secure_filename(file.filename))

    # f.save(secure_filename(f.filename))
    return jsonify(data='file uploaded successfully')


if __name__ == '__main__':
    app.run(debug=True)
