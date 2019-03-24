import blockcypher
import binascii

############################################################################
# Generate a new adress for the bitcoin testnet
# https://coinfaucet.eu/en/btc-testnet/

def generateAddress():
	address_object = blockcypher.generate_new_address(coin_symbol='btc-testnet', api_key= '141dbdc7350f4275900fd063fd56b6d3')
	address = address_object['address']
	public_key = address_object['public']
	private_key = address_object['private']
	print ("address: ", address, "public_key: ", public_key, "private_key: ", private_key)

############################################################################
# Q 2.3
# Create a transaction writing your student id into the blockchain!

############################################################################
# script string is the hex encoding of a suitable script to create a proof of burn 
# transaction with your student id in it (mdsw22)
def proofOfBurnTransaction():
	
	data = "mdsw22"

	# OP RETURN and push data to stack
	prefix = "6a4c"

	# get the size of data in bytes and hex of the data itself
	hexdata = binascii.hexlify(bytes(data, 'ascii'))
	prefix += binascii.hexlify(bytes(chr(len(data)), 'ascii')).decode('ascii')
	prefix += hexdata.decode('ascii')

	inputs = [{'address': 'n1xrgmc48JBh31wYJmRadDyS5Lbh5gGqNu'}]
	outputs = [{'value' : 0, 'script_type':"null-data", 'script':prefix}]

	#The next line creates the transaction shell, which is as yet unsigned
	unsigned_tx = blockcypher.create_unsigned_tx(inputs=inputs, outputs=outputs, coin_symbol='btc-testnet', api_key='141dbdc7350f4275900fd063fd56b6d3')

	#Now list the private and public keys corresponding to the inputs
	private_keys=['61361420f531bf9e0893db1dbc061dcc00a22f5fb38f58d25f0fcaa1731d969e']
	public_keys=['025929058c2e17d1983682cf884e6ee7a6319f5098128badd944a2b441bd82fe9e']

	#Next create the signatures
	tx_signatures = blockcypher.make_tx_signatures(txs_to_sign=unsigned_tx['tosign'], privkey_list=private_keys, pubkey_list=public_keys)

	#Finally push the transaction and signatures onto the network
	result = blockcypher.broadcast_signed_transaction(unsigned_tx=unsigned_tx, signatures=tx_signatures, pubkeys=public_keys, coin_symbol='btc-testnet', api_key='141dbdc7350f4275900fd063fd56b6d3')
	
	# get the transaction hash
	transaction_hash = result['tx']['hash']
	
	return transaction_hash

############################################################################
