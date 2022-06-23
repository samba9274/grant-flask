from os import stat
from flask import Flask, request, Response, jsonify
from datetime import *
from DonationDao import *
from UserDao import *
from Donation import Donation
from Utils import *
from flask_cors import CORS
from User import User
import jwt

app = Flask(__name__)
CORS(app)
jwtSecret = "secret"


@app.route("/donations", methods=["POST"])
def postDonation():
    if request.headers["Authorization"].startswith("Bearer"):
        if getUserById(jwt.decode(request.headers["Authorization"][7:], jwtSecret, algorithms="HS256")["userId"]).role == "USER":
            insertDonation(Donation(getNextDonationId(),
                                    int(request.json['donorUserId']),
                                    request.json['description'],
                                    request.json['images'],
                                    int(request.json['inventory']),
                                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                    None,
                                    None,
                                    "PENDING",
                                    0,
                                    0))
            return Response(status=201)
    return Response(status=403)


@app.route("/donations/<donationId>", methods=['PATCH'])
def patchDonation(donationId):
    if request.headers["Authorization"].startswith("Bearer"):
        if getUserById(jwt.decode(request.headers["Authorization"][7:], jwtSecret, algorithms="HS256")["userId"]).role == "INSTITUTE":
            donation = getDonationById(donationId)
            donation.receiverUserId = request.json['recieveruserId']
            donation.acceptationDate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            donation.donationStatus = "COMPLETED"
            updateDonation(donation)
            return jsonify(getUserById(donation.donorUserId).toDict())
    return Response(status=403)


@app.route("/donations/<donationId>", methods=['DELETE'])
def deleteDonation(donationId):
    if request.headers["Authorization"].startswith("Bearer"):
        donation = getDonationById(donationId)
        if jwt.decode(request.headers["Authorization"][7:], jwtSecret, algorithms="HS256")["userId"] == donation.donorUserId or getUserById(jwt.decode(request.headers["Authorization"][7:], jwtSecret, algorithms="HS256")["userId"]).role == "ADMIN":
            donation.donationStatus = "DELETED"
            updateDonation(donation)
            return Response(status=200)
    return Response(status=403)


@app.route("/donations/report/<donationId>", methods=['PATCH'])
def reportDonation(donationId):
    if request.headers["Authorization"].startswith("Bearer"):
        donation = getDonationById(donationId)
        if getUserById(jwt.decode(request.headers["Authorization"][7:], jwtSecret, algorithms="HS256")["userId"]).role == "INSTITUTE":
            donation.donationStatus = "REPORTED"
            updateDonation(donation)
            return Response(status=200)
    return Response(status=403)


@app.route("/donations", methods=["GET"])
def getDonationsNearInstitute():
    institute = getUserById(request.args['instituteID'])
    if institute:
        donations = getAllPendingDonations()
        for donation in donations:
            donation.distance = calcDistance((donation.latitude, donation.longitude),
                                             (institute.latitude, institute.longitude))
            donation.donorName = getUserById(donation.donorUserId).name
        donations = [donation.toDistanceDict() for donation in donations]
        return jsonify({"donations": donations})
    return Response(status=404)


@app.route("/donations/<status>", methods=["GET"])
def getUserDonations(status):
    donations = getUserDonationsByStatus(request.args['userId'], status)
    if status == "COMPLETED":
        for donation in donations:
            donation.receiverName = getUserById(donation.receiverUserId).name
        donations = [donation.toReceiverDict() for donation in donations]
    else:
        donations = [donation.toDict() for donation in donations]
    return jsonify({"donations": donations})


@app.route("/accepted/<id>", methods=["GET"])
def acceptedDonations(id):
    donations = getAcceptedDonations(id)
    donationsDict = list()
    for donation in donations:
        d = donation.toDict()
        d["donor"] = getUserById(donation.donorUserId).toDict()
        donationsDict.append(d)
    return jsonify({"donations": donationsDict})


@app.route("/reported", methods=["GET"])
def reportedDonations():
    donations = getReportedDonations()
    donationsDict = list()
    for donation in donations:
        d = donation.toDict()
        d["donor"] = getUserById(donation.donorUserId).toDict()
        donationsDict.append(d)
    return jsonify({"donations": donationsDict})


@app.route('/validate', methods=['POST'])
def login():
    user = getUserByEmail(request.json["email"])
    if user.password == request.json["password"]:
        return {"role": user.role,
                "jwt": jwt.encode({"userId": user.userId}, jwtSecret),
                "userId": user.userId}
    return Response(status=403)


@app.route('/emails', methods=['GET'])
def CheckEmail():
    emails = getAllEmails()
    if request.args["email"] in emails:
        return False
    return True


@app.route('/report', methods=['GET'])
def getReport():
    if request.headers["Authorization"].startswith("Bearer"):
        if getUserById(jwt.decode(request.headers["Authorization"][7:], jwtSecret, algorithms="HS256")["userId"]).role == "ADMIN":
            report = fetchReport()
            print(report)
            return report
    return Response(status=403)


@ app.route('/users', methods=['POST'])
def user():
    insertUser(User(getNextuserId(),
                    request.json["name"],
                    request.json["email"],
                    request.json["password"],
                    request.json["mobile"],
                    request.json["latitude"],
                    request.json["longitude"],
                    "USER"))
    return Response(status=201)


@ app.route('/institute', methods=['POST'])
def institute():
    if request.headers["Authorization"].startswith("Bearer"):
        if getUserById(jwt.decode(request.headers["Authorization"][7:], jwtSecret, algorithms="HS256")["userId"]).role == "ADMIN":
            insertUser(User(getNextuserId(),
                            request.json["name"],
                            request.json["email"],
                            request.json["password"],
                            request.json["mobile"],
                            request.json["latitude"],
                            request.json["longitude"],
                            "INSTITUTE"))
        return Response(status=201)
    return Response(status=403)


if __name__ == "__main__":
    app.run(debug=True)
