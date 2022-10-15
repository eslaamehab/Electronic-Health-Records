from calendar import c
from copyreg import constructor
from mimetypes import init
from black import nullcontext
from eth_typing import Address
from solcx import compile_standard
import json
from web3 import Web3
import web3
import time
import os
import rsa
import Crypto.PublicKey.RSA
from AESenc import AESCipher

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.6.0",
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)


# get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# get abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# for connecting to ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
chain_id = 1337
# my_address = "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1"
# private_key = "0x4f3edf983ac636a65a842ce7c78d9aa706d3b113bce9c46f30d7d21715b23b1d"
my_address = "0xf72C09C4e0E4106503c6fE9fc93C66B2a4A743ff"
private_key = "0x3e95f838f062b28e8914531cf0b62177e993451915b25f21131b111f650f5ad9"
# Create the contract in python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)


def verify(message, signature, key):
    try:
        return (
            rsa.verify(
                message.encode("ascii"),
                signature,
                key,
            )
            == "SHA-1"
        )
    except:
        return False


def loadKeys(doctor_id):
    with open("keys/" + str(doctor_id) + "-publicKey.pem", "rb") as p:
        publicKey = rsa.PublicKey.load_pkcs1(p.read())
    return publicKey


def getVisits(patient_id, doctor_id):
    lastB = w3.eth.get_block_number()
    block = w3.eth.get_block(lastB, True)

    previousBlockAddress = b""

    print("Visits:")
    PreviousVisits = []
    while lastB >= 1:
        tx_recepit = w3.eth.get_transaction_receipt(block.transactions[0].hash)
        current_contract = w3.eth.contract(address=tx_recepit.contractAddress, abi=abi)
        (
            lastPatientId,
            doctorid,
            retrievedname,
            retrievedage,
            retrievedsex,
            retrievedheight,
            retrievedweight,
            readings,
            previousBlockAddress,
        ) = current_contract.functions.retrieve().call(
            {"from": w3.toChecksumAddress(my_address)}
        )
        if patient_id == lastPatientId:
            if doctorid != doctor_id:
                print("Doctor DOES NOT have access to view patient")
                return False
            previousBlockAddress = block.transactions[0].hash
            PreviousVisits.append(
                {
                    lastPatientId,
                    doctorid,
                    retrievedname,
                    retrievedage,
                    retrievedsex,
                    retrievedheight,
                    retrievedweight,
                    readings,
                }
            )
            lastB = lastB - 1
            block = w3.eth.get_block(lastB, True)

            # print(block.transactions[0].hash)
            # print(previousBlockAddress)
            # if previousBlockAddress.decode("utf-8") == "":
            #     print("yeaaaahhhh")
            # while previousBlockAddress.decode("utf-8") != "":
            #     tx_recepit = w3.eth.get_transaction_receipt(previousBlockAddress)
            #     current_contract = w3.eth.contract(
            #         address=tx_recepit.contractAddress, abi=abi
            #     )
            #     (
            #         lastPatientId,
            #         doctorid,
            #         retrievedname,
            #         retrievedsex,
            #         retrievedheight,
            #         retrievedweight,
            #         retrievedage,
            #         readings,
            #         previousBlockAddress,
            #     ) = current_contract.functions.retrieve().call(
            #         {"from": w3.toChecksumAddress(my_address)}
            #     )
            #     if patient_id == lastPatientId:
            #         previousBlockAddress = block.transactions[0].hash
            #         PreviousVisits.append(
            #             {
            #                 lastPatientId,
            #                 doctorid,
            #                 retrievedname,
            #                 retrievedsex,
            #                 retrievedheight,
            #                 retrievedweight,
            #                 retrievedage,
            #                 readings,
            #             }
            #         )
            # break

        else:
            lastB = lastB - 1
            block = w3.eth.get_block(lastB, True)
    print(PreviousVisits)
    return PreviousVisits


def StorePatient(
    patient_id,
    doctor_id,
    signature,
    EName,
    EAge,
    ESex,
    EHeight,
    EReadings,
    EWeight,
):
    doctorPublicKey = loadKeys(doctor_id)
    validatedName = verify(EName, signature, doctorPublicKey)

    if validatedName == False:
        print("Wrong DR id")
        return

    print("Doctor is Verified")

    latestBlock = w3.eth.get_block_number()
    block = w3.eth.get_block(latestBlock, True)

    previousBlockAddress = b""

    while latestBlock >= 1:
        tx_recepit = w3.eth.get_transaction_receipt(block.transactions[0].hash)
        current_contract = w3.eth.contract(address=tx_recepit.contractAddress, abi=abi)
        (
            lastPatientId,
            lastdoctor_id,
            name,
            lastheight,
            lastsex,
            lastweight,
            lastpatientage,
            lastpatientreadings,
            previousBlockAddress,
        ) = current_contract.functions.retrieve().call(
            {"from": w3.toChecksumAddress(my_address)}
        )
        if patient_id == lastPatientId:
            previousBlockAddress = block.transactions[0].hash
            break
        else:
            latestBlock = latestBlock - 1
            block = w3.eth.get_block(latestBlock, True)

    cipher = AESCipher("Encryption Key")

    decrypted_name = cipher.decrypt(EName)
    decrypted_age = cipher.decrypt(EAge)
    decrypted_sex = cipher.decrypt(ESex)
    decrypted_height = cipher.decrypt(EHeight)
    decrypted_readings = cipher.decrypt(EReadings)
    decrypted_weight = cipher.decrypt(EWeight)
    print(
        "name:",
        decrypted_name + " ",
        "age:",
        decrypted_age + " ",
        "sex:",
        decrypted_sex + " ",
        "height:",
        decrypted_height + " ",
        "weight: ",
        decrypted_weight + " ",
        "readings:",
        decrypted_readings + " ",
    )

    # Create the contract in Python
    SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

    # Get the latest transaction
    nonce = w3.eth.get_transaction_count(my_address)

    # Submit the transaction that deploys the contract
    transaction = SimpleStorage.constructor(
        patient_id,
        doctor_id,
        decrypted_name,
        decrypted_age,
        decrypted_sex,
        decrypted_height,
        decrypted_weight,
        decrypted_readings,
        previousBlockAddress,
    ).build_transaction(
        {
            "gasPrice": w3.eth.gas_price,
            "chainId": chain_id,
            "from": my_address,
            "nonce": nonce,
        }
    )

    # Sign the transaction
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key)
    # Send it!
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    # Wait for the transaction to be mined, and get the transaction receipt
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    # Working with deployed Contracts
    simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

    print(simple_storage.functions.retrieve().call())
