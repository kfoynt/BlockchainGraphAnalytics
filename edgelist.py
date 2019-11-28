from web3.auto.infura import w3
import json
import sys
import requests
import argparse
from requests.exceptions import HTTPError
import eth_utils

from datetime import datetime

from transaction import Transaction
import constant

GET_ACCOUNT_NORMAL_TRANSACTION_URL = 'http://api.etherscan.io/api?module=account&action=txlist&address={}&startblock={}&endblock=99999999&sort=asc'
ETHERSCAN_URL = 'http://etherscan.io/address/{}'

WEI = 1000000000000000000
EXCHANGE_LIST = list(constant.EXCHANGE_DICT.values())

total_address_set = set()
total_transaction_set = set()


def get_ether_transaction(account, startBlock, endBlock):
  try:
    response = requests.get(GET_ACCOUNT_NORMAL_TRANSACTION_URL.format(account, startBlock, endBlock))
    response.raise_for_status()

  except HTTPError as http_err:
    print(f'HTTP error occurred: {http_err}') 
    sys.exit(0)
  except Exception as err:
    print(f'Other error occurred: {err}')
    sys.exit(0)
  else:
    json_res = json.loads(response.text)
    res_set = set()
    address_set = set()

    if not json_res['result']:
      print(f'{account} has no transactions')
      return res_set
    else:

      for transaction in json_res['result']:
        if(not transaction['contractAddress'] and transaction['isError'] == '0' and transaction['input'] == '0x'):

          if(transaction['from'] != transaction['to'] and predicate_internal_transaction(transaction['to']) and predicate_internal_transaction(transaction['from'])):
            transaction_object = Transaction(transaction['from'], transaction['to'], transaction['value'], 
            transaction['gas'], transaction['gasPrice'], transaction['hash'])

            if transaction['from'] not in EXCHANGE_LIST:
              address_set.add(transaction['from'])
            if transaction['to'] not in EXCHANGE_LIST:
              address_set.add(transaction['to'])
            if transaction['from'] not in EXCHANGE_LIST and transaction['to'] not in EXCHANGE_LIST:
              res_set.add(transaction_object);
            
      print (f'Get all transactions for {account}')
      return (res_set, address_set)


def predicate_internal_transaction(account):
  return (w3.eth.getCode(w3.toChecksumAddress(account))) == b''
  

def get_multiple_layers_ether_transaction(account, layer = 2, startBlock = 0 , endBlock = 999999999):
  total_address_set.add(account)

  current_transaction_set, current_address_set = get_ether_transaction(account, startBlock, endBlock)
  total_transaction_set.update(current_transaction_set)
  
  # BFS
  for i in range(1, layer):
    current_layer_address_set = current_address_set - total_address_set
    total_address_set.update(current_address_set)

    for address in current_layer_address_set:
      temp_transaction_set, temp_address_set = get_ether_transaction(address, startBlock, endBlock)
      current_address_set.update(temp_address_set)
      total_transaction_set.update(temp_transaction_set)

  total_address_set.update(current_address_set)


def generate_edgelist(nickname):
  total_address_list = list(total_address_set)
  f1 = open(f"data/{nickname}.edgelist","w+")

  for transaction in total_transaction_set:
    gas_total = int(transaction.value)/WEI + int(transaction.gas)/WEI * int(transaction.gasPrice)/WEI
    f1.write(str(total_address_list.index(transaction.fromAddress)) + '\t' + str(total_address_list.index(transaction.toAddress)) + '\t' 
    + str(gas_total) + '\n')
  f1.close

  f2 = open(f"data/{nickname}_address.txt","w+")

  for address in total_address_set:
    f2.write(address + '\t' + str(total_address_list.index(address)) + "\n")
  f2.close


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Ethereum network graph generater')
  parser.add_argument('address', nargs=1, help='the address that want to investigate')
  parser.add_argument('layer', nargs=1, type=int, help='the number of layer that the address search, 1 layer means just searching neighbours')
  parser.add_argument('-n', nargs=1, help='the nickname of the address')
  args = parser.parse_args()

  address = args.address[0]
  layer = args.layer[0]

  if not eth_utils.is_hex_address(address):
    print (f'{address} is not a valid address')
    sys.exit(0)
  if not args.n:
    dateTimeObj = datetime.now()
    nickname = dateTimeObj.strftime("%d-%m-%Y-%H:%M:%S")
  else:
    nickname = args.n[0]
  
  get_multiple_layers_ether_transaction(eth_utils.to_normalized_address(address), layer)
  generate_edgelist(nickname)
