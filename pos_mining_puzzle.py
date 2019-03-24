import hashlib
import ecdsa
import json 

# An the previous block header - do not change any fields
previous_block_header = {
  "previousBlockHash": "651c16a0226d2ddd961c9391dc11f703c5972f05805c4fb45ab1469dda1d4b98",
  "payloadLength": 209,
  "totalAmountNQT": "383113873926",
  "generationSignature": "9737957703d4eb54efdff91e15343266123c5f15aaf033292c9903015af817f1",
  "generator": "11551286933940986965",
  "generatorPublicKey": "feb823bac150e799fbfc124564d4c1a72b920ec26ce11a07e3efda51ca9a425f",
  "baseTarget": 1229782938247303,
  "payloadHash": "06888a0c41b43ad79c4e4991e69372ad4ee34da10d6d26f30bc93ebdf7be5be0",
  "generatorRS": "NXT-MT4P-AHG4-A4NA-CCMM2",
  "nextBlock": "6910370859487179428",
  "requestProcessingTime": 0,
  "numberOfTransactions": 1,
  "blockSignature": "0d237dadff3024928ea4e5e33613413f73191f04b25bad6b028edb97711cbd08c525c374c3e2684ce149a9abb186b784437d01e2ad13046593e0e840fd184a60",
  "transactions": ["14074549945874501524"],
  "version": 3,
  "totalFeeNQT": "200000000",
  "previousBlock": "15937514651816172645",
  "cumulativeDifficulty": "52911101533010235",
  "block": "662053617327350744",
  "height": 2254868,
  "timestamp": 165541326
}

# you should edit the effective balance to be the last two digits from your user id
effective_balance = 22

############################################################################
# generate a signing key pair 
def generateKeyPair():

    # sk is the signing key (private)
    sk = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)

    # vk is the verifying key (public)
    vk = sk.get_verifying_key()

    return sk, vk

############################################################################
# sign a message
def signBlock(message, sk):

    # encode the string as a bytes
    message_bytes = str.encode(message)

    # sign a byte encoded message with private key
    sig = sk.sign(message_bytes)

    # return the signature and the verifying key
    return sig

############################################################################
# verify a signature
def verifySignature(vk, sig, message):
    message_bytes = str.encode(message)
    # assert whether true 
    assert vk.verify(sig, message_bytes)

############################################################################
# gets the values to pass into verify.py
def checkSignaturesWorking():
    sk, vk = generateKeyPair()
    data_block = "Hello world"
    sig = signBlock(data_block, sk)
    verifySignature(vk, sig, data_block)

    # this gets the public key as a hex
    vk_string=(vk.to_string()).hex()
    # gets signature as hex string
    sig_string = sig.hex()

    return 

############################################################################
# To mine you sign the previous block generation signature with your private key
# hash the result, and take the first 8 bytes.
# This is your hit value (in hex)
def computeHitValue(previous_block_header, sk):

    # get the previous block generation signature 
    prev_block_gen_sig = previous_block_header['generationSignature']

    print ("prev_block_gen_sig: " + prev_block_gen_sig)

    # sign prev_block_gen_sig with private key
    sig = signBlock(prev_block_gen_sig, sk)

    # this prints the signature in hex
    print ("sig: " + sig.hex())

    # hash the result (hex digest)
    # 256 bits is 32 bytes
    # each hex digit represents half a byte
    # therefore 64 hex digits to represent 32 byte hash
    sig_hash = hashlib.sha256(sig).hexdigest()

    print ("sig hash: " + str(sig_hash))

    # to get first 8 bytes must take first 16 characters of hex 
    hit_value = sig_hash[:16]

    # return the hit_value in hex
    return hit_value

############################################################################
# Calculates target value, based on current effective stake. 
def computeTargetValue(previous_block_header, timeSinceLastBlock):

    # get the effective_balance as global variable (should = 22)
    global effective_balance

    # base target value from block header 
    baseTargetValue = previous_block_header['baseTarget']
    targetValue = effective_balance * baseTargetValue * timeSinceLastBlock
    return targetValue

############################################################################
# when the hit value is less than the target you can create a block
def computeTimeToForgeNewBlock(previous_block_header, sk):

    # compute hit value 
    hit_value = computeHitValue(previous_block_header, sk)

    print ("hit value: " + hit_value)

    # transform hit value into an int 
    hit_value_int = int(hit_value, 16)

    # increment time (s) in loop
    timeSinceLastBlock = 0
    while True:
        targetValue = computeTargetValue(previous_block_header, timeSinceLastBlock)
        if hit_value_int < targetValue:
            break
        else:
            timeSinceLastBlock += 1
            continue
    return timeSinceLastBlock

############################################################################


#generate signing key pair
sk, vk = generateKeyPair()


'''
sig = signBlock("Hello world", sk)
print ("sig: ")
print (sig.hex())
print ("signing key: ")
sk_string=(sk.to_string()).hex()
print (sk_string)

print ("verifying  key: ")
vk_string=(vk.to_string()).hex()
print (vk_string)
'''

timeSinceLastBlock = computeTimeToForgeNewBlock(previous_block_header, sk)
print ("time sinece last block: " + str(timeSinceLastBlock))

############################################################################
