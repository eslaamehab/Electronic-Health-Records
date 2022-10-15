from deploy import StorePatient, getVisits
from AESenc import AESCipher
import rsa


# PATIENTS
class Patient:
    def __init__(self):
        self.name = None
        self.sex = None
        self.age = None
        self.height = None
        self.weight = None
        self.readings = None
        self.id = None
        self.doctor_id = None


class Doctor(object):
    def __init__(self, id, name):
        (publicKey, privateKey) = rsa.newkeys(1024)
        with open("keys/" + str(id) + "-publicKey.pem", "wb") as p:
            p.write(publicKey.save_pkcs1("PEM"))
        self.privateKey = privateKey
        self.name = name
        self.id = id


doctor1 = Doctor(1, "DR1")
doctor2 = Doctor(2, "DR2")


def sign(message, key):
    return rsa.sign(message.encode("ascii"), key, "SHA-1")


cipher = AESCipher("Encryption Key")

# Patient
patient = Patient()
patient.id = 2
patient.doctor_id = 2
patient.name = "aly"
patient.sex = "male"
patient.weight = "65"
patient.height = "175"
patient.readings = "none"
patient.age = "22"

encrypted_name = cipher.encrypt(patient.name)
encrypted_age = cipher.encrypt(patient.age)
encrypted_sex = cipher.encrypt(patient.sex)
encrypted_height = cipher.encrypt(patient.height)
encrypted_weight = cipher.encrypt(patient.weight)
encrypted_readings = cipher.encrypt(patient.readings)


signature = sign(encrypted_name.decode("utf-8"), doctor2.privateKey)

StorePatient(
    patient.id,
    doctor2.id,
    signature,
    encrypted_name.decode("utf-8"),
    encrypted_age.decode("utf-8"),
    encrypted_sex.decode("utf-8"),
    encrypted_height.decode("utf-8"),
    encrypted_readings.decode("utf-8"),
    encrypted_weight.decode("utf-8"),
)

getVisits(2, 2)
