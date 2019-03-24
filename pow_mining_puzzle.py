import hashlib
import json
import time

############################################################################
# Crypto Assignment
# Please use Python 3!

############################################################################
example_block_header = {'height': 1478503,
                        'prev_block': '0000000000000da6cff8a34298ddb42e80204669367b781c87c88cf00787fcf6',
                        'total': 38982714093,
                        'fees': 36351,
                        'size': 484,
                        'ver': 536870912,
                        'time': 1550603039.882228,
                        'bits': 437239872,
                        'nonce': 0,                    
                        'coinbase_addr': 'mdsw22',     
                        'n_tx': 2,
                        'mrkl_root': '69224771b7a2ed554b28857ed85a94b088dc3d89b53c2127bfc5c16ff49da229',
                        'txids': ['3f9dfc50198cf9c2b0328cd1452513e3953693708417440cd921ae18616f0bfc', '3352ead356030b335af000ed4e9030d487bf943089fc0912635f2bb020261e7f'],
                        'depth': 0
                        }

############################################################################
# double hash the serialized block
def double_hash_block(block_serialised):
    block_hash = hashlib.sha256(hashlib.sha256(block_serialised).digest()).hexdigest()
    return block_hash

############################################################################
# serialise data block
def serialiseDataBlock(data_block):
    serialised_data_block = json.dumps(data_block, sort_keys=True).encode()
    return serialised_data_block

############################################################################
def compute_target_value(difficulty = 0.001):

    # initial target
    initial_target_hex = 0x00000000FFFF0000000000000000000000000000000000000000000000000000

    # target = initial_target / difficult 
    target = initial_target_hex / difficulty

    # convert target to hex 
    target_in_hex = hex(int(target))

    return target_in_hex

############################################################################
# Compute the target when difficult is 0.001
# 0x3e7fc180000000000000000000000000000000000000000000000000000

############################################################################
def proof_of_work(block_header, target):
    nonce = 0
    while valid_proof(block_header, nonce, target) is False:
        nonce += 1
    return nonce

############################################################################
# find a valid nonce (i.e. check for valid proof)
def valid_proof(block_header, nonce, target):

    # get the nonce in the block header
    block_header['nonce'] = nonce

    # serialise the block header 
    serialised_block = serialiseDataBlock(block_header)

    # double hash the block header (returns hash digest in hex)
    block_header_hash_hex = double_hash_block(serialised_block)

    # convert hex to int 
    block_header_hash_int = int(block_header_hash_hex, 16)

    # covert target to int
    target_int = int(target, 16)

    # return true if block header hash is less than the target 
    return block_header_hash_int < target_int

############################################################################

target = compute_target_value()
print ("target: " + target)

start = time.time()
nonce = proof_of_work(example_block_header, target)
print (nonce)
end = time.time()
print(end - start)


