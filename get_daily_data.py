from web3 import Web3
import os
from dotenv import load_dotenv
import requests
import json
import pandas as pd
import numpy as np

load_dotenv()
ES_API_KEY = os.getenv('ETHERSCAN_API_KEY')

address_list = [
    "0x4c6f947Ae67F572afa4ae0730947DE7C874F95Ef",
    "0x51de512aa5dfb02143a91c6f772261623ae64564",
    '0x4BF681894abEc828B212C906082B444Ceb2f6cf6',
    '0x5E4e65926BA27467555EB562121fac00D24E9dD2',
    '0xBe5dAb4A2e9cd0F27300dB4aB94BeE3A233AEB19',
    '0x0d62bac5c346c78DC1b27107CAbC5F4DE057a830',
    '0xD54f502e184B6B739d7D27a6410a67dc462D69c8',
    '0xC8c212f11f6ACca77A7afeB7282dEBa5530eb46C',
    '0xEfbCcE4659db72eC6897F46783303708cf9ACef8',
    '0xf6b83CcaDeee478FC372AF6ca7069b14FBc5E1B1',
    '0x2cAbD63F6f28b493f33D13E34060f0959F3570aE',
    '0x6dE5bDC580f55Bc9dAcaFCB67b91674040A247e3',
    '0x5CDAF83E077DBaC2692b5864CA18b61d67453Be8',
    '0x5d22045DAcEAB03B158031eCB7D9d06Fad24609b',
    '0x737901bea3eeb88459df9ef1BE8fF3Ae1B42A2ba',
    '0xA68D85dF56E733A06443306A095646317B5Fa633',
    '0xabea9132b05a70803a4e85094fd0e1800777fbef',
    '0x18c208921F7a741510a7fc0CfA51E941735DAE54',
    '0xda7357bBCe5e8C616Bc7B0C3C86f0C71c5b4EaBb',
    '0x153CdDD727e407Cb951f728F24bEB9A5FaaA8512',
    '0x5FDCCA53617f4d2b9134B29090C87D01058e27e9',
    '0x17834b754e2f09946CE48D7B5beB4D7D94D98aB6',
    '0xfBd2541e316948B259264c02f370eD088E04c3Db',
    '0x56a76bcC92361f6DF8D75476feD8843EdC70e1C9',
    '0xf209815E595Cdf3ed0aAF9665b1772e608AB9380',
    '0x2C169DFe5fBbA12957Bdd0Ba47d9CEDbFE260CA7',
    '0xc662c410C0ECf747543f5bA90660f6ABeBD9C8c4',
    '0x96375087b2F6eFc59e5e0dd5111B4d090EBFDD8B'
]

test_list = address_list[:2]


# function that uses etherscan API to give us the block fat a given timestamp
def getBlockFromTimestamp(timestamp):
    request = f"https://api.etherscan.io/api?module=block&action=getblocknobytime&timestamp={timestamp}&closest=before&apikey={ES_API_KEY}"
    response = requests.get(request)
    data = response.json()
    return data['result']

# dates have to be close apart (I would use 1 day apart)
# parameters
    # startTimestamp: unix timestamp of start
    # endTimestamp: unix timestamp of end
    # address: address of contract to check gas spent on
# returns
    # total gas used


def gasUsedBetween(startTimestamp, endTimestamp, address):
    startBlock = getBlockFromTimestamp(startTimestamp)
    endBlock = getBlockFromTimestamp(endTimestamp)
    OFFSET = 1000  # MAX number of results between start and end dates

    gas_array = []
    timestamp_array = []
    hash_array = []

    request = f"https://api.etherscan.io/api?module=account&action=txlist&address={address}&startblock={startBlock}&endblock={endBlock}&page=1&offset={OFFSET}&sort=asc&apikey={ES_API_KEY}"
    response = requests.get(request)
    data = response.json()

    for i in range(len(data['result'])):
        gas_array.append(data['result'][i]['gasUsed'])
        timestamp_array.append(data['result'][i]['timeStamp'])
        hash_array.append(data['result'][i]['hash'])

    print_data = False

    if(print_data):
        print(gas_array)
        print(timestamp_array)
        print(hash_array)
        print(len(gas_array))

    gas_array = [int(x) for x in gas_array]
    total_gas_used = np.sum(gas_array)

    return total_gas_used


print(gasUsedBetween(1661241185, 1661245479,
      "0x51de512aa5dfb02143a91c6f772261623ae64564"))

print(test_list)


# ONLY WORKS FOR SHORT TIMESTAMPS (E.G. DAILY DATA UPDATING)
# todo: write function that takes a list of addresses and sums them up
# parameters
# startTimestamp: unix timestamp of start
# endTimestamp: unix timestamp of end
# addressList: address list of contracts to sum gas spent on
# returns
# total gas used across contracts on list
def L2gasUsedBetween(startTimestamp, endTimestamp, addressList):
    totalGas = 0

    for address in addressList:
        gas = gasUsedBetween(startTimestamp, endTimestamp, address)
        totalGas += gas

    return totalGas


# example usage
def main():
    # returns the gas used of 2nd address in address_list between the two timestamps.
    # should return the gas used in only one transaction, here: https://etherscan.io/tx/0x7fc3bcec6138321ced46ee7ed64c80d04e59de825aaa59b715d6e5c737eb382a
    print(gasUsedBetween(1661241185, 1661245479,
                         address_list[1]))

    # return the total gas used of the 2 addresses in test_list
    print(L2gasUsedBetween(1661241185, 1661245479, test_list))
