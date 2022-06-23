from Donation import Donation
import psycopg2


conn = psycopg2.connect(
    host="ec2-99-80-170-190.eu-west-1.compute.amazonaws.com",
    database="dbv0gpvc5od45q",
    user="frkhrhwhzkvmri",
    password="226d1bf6214abd70d5bb474fb790d84b3676709837180606c3d92a107c6c8d6e")

mycursor = conn.cursor()


def getNextDonationId():
    mycursor = conn.cursor()
    mycursor.execute("select max(donationId) from donations")
    r = mycursor.fetchone()
    if r[0]:
        return r[0]+1
    return 1


def getNextImageId():
    mycursor = conn.cursor()
    mycursor.execute("select max(imageId) from images")
    r = mycursor.fetchone()
    if r[0]:
        return r[0]+1
    return 1


def insertDonation(donation):
    mycursor.execute("INSERT INTO donations VALUES(%s, %s, %s, %s, %s, %s, %s, %s)", (donation.donationId,
                                                                                      donation.donorUserId,
                                                                                      donation.description,
                                                                                      donation.inventory,
                                                                                      donation.donationDate,
                                                                                      donation.receiverUserId,
                                                                                      donation.acceptationDate,
                                                                                      donation.donationStatus))
    for image in donation.images:
        mycursor.execute("INSERT INTO images VALUES(%s, %s, %s)", (getNextImageId(),
                                                                   donation.donationId,
                                                                   image))
    mydb.commit()


def updateDonation(donation):
    mycursor.execute("UPDATE donations SET donoruserId=%s, description=%s, inventory=%s, donationDate=%s, recieveruserId=%s, acceptationDate=%s, donationStatus=%s WHERE donationId=%s", (donation.donorUserId,
                                                                                                                                                                                          donation.description,
                                                                                                                                                                                          donation.inventory,
                                                                                                                                                                                          donation.donationDate,
                                                                                                                                                                                          donation.receiverUserId,
                                                                                                                                                                                          donation.acceptationDate,
                                                                                                                                                                                          donation.donationStatus,
                                                                                                                                                                                          donation.donationId))
    mydb.commit()


def getDonationById(id):
    mycursor.execute(
        "SELECT * FROM donations WHERE donationId=%s", tuple([id]))
    donationTuple = mycursor.fetchone()
    donation = Donation(donationTuple[0], donationTuple[1], donationTuple[2], None, donationTuple[3],
                        donationTuple[4], donationTuple[5], donationTuple[6], donationTuple[7], 0, 0)
    mycursor.execute(
        "SELECT image FROM images WHERE donationId=%s", tuple([id]))
    donation.images = [str(img)[3:-3] for img in mycursor.fetchall()]
    return donation


def getAllPendingDonations():
    mycursor.execute('SELECT donations.donationId, donations.donoruserId, donations.description, donations.inventory, donations.donationDate, donations.recieveruserId, donations.acceptationDate, donations.donationStatus, users.latitude, users.longitude FROM donations INNER JOIN users ON donations.donoruserId=users.userId WHERE donations.donationStatus="PENDING"')
    donationTuples = mycursor.fetchall()
    donations = [Donation(donation[0], donation[1], donation[2], None, donation[3],
                          donation[4], donation[5], donation[6], donation[7], donation[8], donation[9]) for donation in donationTuples]
    for donation in donations:
        mycursor.execute(
            "SELECT image FROM images WHERE donationId=%s", tuple([donation.donationId]))
        donation.images = [str(img)[3:-3] for img in mycursor.fetchall()]
    return donations


def getUserDonationsByStatus(userId, status):
    mycursor.execute(
        'SELECT * FROM donations WHERE donoruserId={} AND donationStatus=%s'.format(userId), tuple([status]))
    donationTuples = mycursor.fetchall()
    donations = [Donation(donation[0], donation[1], donation[2], None, donation[3], donation[4],
                          donation[5], donation[6], donation[7], 0, 0) for donation in donationTuples]
    for donation in donations:
        mycursor.execute(
            "SELECT image FROM images WHERE donationId=%s", tuple([donation.donationId]))
        donation.images = [str(img)[3:-3] for img in mycursor.fetchall()]
    return donations


def getAcceptedDonations(id):
    mycursor.execute(
        "SELECT * FROM donations WHERE recieveruserId=%s", tuple([id]))
    donationTuples = mycursor.fetchall()
    donations = [Donation(donation[0], donation[1], donation[2], None, donation[3], donation[4],
                          donation[5], donation[6], donation[7], 0, 0) for donation in donationTuples]
    for donation in donations:
        mycursor.execute(
            "SELECT image FROM images WHERE donationId=%s", tuple([donation.donationId]))
        donation.images = [str(img)[3:-3] for img in mycursor.fetchall()]
    return donations


def getReportedDonations():
    mycursor.execute('SELECT * FROM donations WHERE donationStatus="Reported"')
    donationTuples = mycursor.fetchall()
    donations = [Donation(donation[0], donation[1], donation[2], None, donation[3], donation[4],
                          donation[5], donation[6], donation[7], 0, 0) for donation in donationTuples]
    for donation in donations:
        mycursor.execute(
            "SELECT image FROM images WHERE donationId=%s", tuple([donation.donationId]))
        donation.images = [str(img)[3:-3] for img in mycursor.fetchall()]
    return donations
