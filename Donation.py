class Donation:
    def __init__(self, donationId, donorUserId, description, images, inventory, donationDate, receiverUserId, acceptationDate, donationStatus):
        self.donationId = donationId
        self.donorUserId = donorUserId
        self.description = description
        self.images = images
        self.inventory = inventory
        self.donationDate = donationDate
        self.receiverUserId = receiverUserId
        self.acceptationDate = acceptationDate
        self.donationStatus = donationStatus

    def __init__(self, donationId, donorUserId, description, images, inventory, donationDate, receiverUserId, acceptationDate, donationStatus, latitude, longitude):
        self.donationId = donationId
        self.donorUserId = donorUserId
        self.description = description
        self.images = images
        self.inventory = inventory
        self.donationDate = donationDate
        self.receiverUserId = receiverUserId
        self.acceptationDate = acceptationDate
        self.donationStatus = donationStatus
        self.latitude = latitude
        self.longitude = longitude

    def toDict(self):
        return {"donationId": self.donationId,
                "donorUserId": self.donorUserId,
                "description": self.description,
                "images": self.images,
                "inventory": self.inventory,
                "donationDate": self.donationDate,
                "receiverUserId": self.receiverUserId,
                "acceptationDate": self.acceptationDate,
                "donationStatus": self.donationStatus}

    def toDistanceDict(self):
        return {"donationId": self.donationId,
                "donorUserId": self.donorUserId,
                "donorName": self.donorName,
                "description": self.description,
                "images": self.images,
                "inventory": self.inventory,
                "donationDate": self.donationDate,
                "receiverUserId": self.receiverUserId,
                "acceptationDate": self.acceptationDate,
                "donationStatus": self.donationStatus,
                "distance": self.distance}

    def toReceiverDict(self):
        return {"donationId": self.donationId,
                "donorUserId": self.donorUserId,
                "receiverName": self.receiverName,
                "description": self.description,
                "images": self.images,
                "inventory": self.inventory,
                "donationDate": self.donationDate,
                "receiverUserId": self.receiverUserId,
                "acceptationDate": self.acceptationDate,
                "donationStatus": self.donationStatus}

    def toLocationDict(self):
        return {"donationId": self.donationId,
                "donorUserId": self.donorUserId,
                "description": self.description,
                "images": self.images,
                "inventory": self.inventory,
                "donationDate": self.donationDate,
                "receiverUserId": self.receiverUserId,
                "acceptationDate": self.acceptationDate,
                "donationStatus": self.donationStatus,
                "latitude": self.latitude,
                "longitude": self.longitude}
