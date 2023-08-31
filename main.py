import json
import requests
import re
import time
import os

network_api_urls = [("https://api.blockchair.com/bitcoin/nodes", 'bitcoin'),
                    ("https://api.blockchair.com/bitcoin-cash/nodes", 'bitcoin-cash'),
                    ("https://api.blockchair.com/bitcoin-sv/nodes", 'bitcoin-sv'),
                    ("https://api.blockchair.com/litecoin/nodes", 'litecoin'),
                    ("https://api.blockchair.com/dogecoin/nodes", 'dogecoin'),
                    ("https://api.blockchair.com/dash/nodes", 'dash'),
                    ("https://api.blockchair.com/groestlcoin/nodes", 'groestlcoin'),
                    ("https://api.blockchair.com/zcash/nodes", 'zcash')
                    ]
ipv6_regex = "([A-Za-z0-9]{1,4}:{1,2}[A-Za-z0-9]{0,4}:{0,2}[A-Za-z0-9]{0,4}:{0,2}[A-Za-z0-9]{0,4}:{0,2}[A-Za-z0-9]{0,4}:{0,2}[A-Za-z0-9]{0,4}:{0,2}[A-Za-z0-9]{0,4}:{1,3}[A-Za-z0-9]{0,4})(?=:8333)"
count = 0


def extractIPs(network_api_urls):
    global count

    os.makedirs("Results/", exist_ok=True)
    for (network, nwName) in network_api_urls:
        response = requests.get(network)
        json_response = json.loads(response.text)
        nodes = json_response['data']['nodes']
        totalIPs = json_response['data']['count']

        addresses = re.findall(ipv6_regex, str(nodes))
        v6IPs = len(addresses)
        ipv6Percentage = v6IPs/totalIPs * 100

        count += 1
        with open(f"Results/Survey#{count}__{nwName}__total#{totalIPs}_IPv6#{v6IPs}_IPv6%{round(ipv6Percentage, 2)}.txt", 'w') as file:
            for address in addresses:
                file.write(address + "\n")
            file.close()
        print(f"Wrote file {count} ({nwName}):\n\tFound {totalIPs} total IP addresses\n\tFound {v6IPs} IPv6 addresses\n\tPercent-wise: {round(ipv6Percentage, 2)}% IPv6 addresses")
    return


if __name__ == '__main__':
    for i in range(10):  # run 10 times total
        extractIPs(network_api_urls=network_api_urls)
        time.sleep(60 * 20)  # run in 20min intervals
