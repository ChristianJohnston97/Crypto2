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

# Q 2.2
# Create a transaction sending 100 Satoshis to the address

############################################################################
# Create a transaction sending amount BTC to specific output address
# must copy in myAddress, private key and public key
def createTransaction(outputAddress, amount):
	#Specify the inputs and outputs below
	#Specify an address, and the backend will work out what transaction output that address has available to spend
	#You do not need to list a change address
	#the transaction will be created with all change (minus the fees) going to the first input address
	inputs = [{'address': 'n1xrgmc48JBh31wYJmRadDyS5Lbh5gGqNu'}]
	outputs = [{'address': outputAddress, 'value': amount}]

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

#createTransaction('mpamtqLA66JFVSQNDaPHZ5xMiCz6T2MeNn', 100)

