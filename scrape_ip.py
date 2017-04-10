# This uses second and third placeholder in the address for hashing
# That is in 10.102.33.44 it uses 102 and 33 for hashing
# into base 256, i.e. 102*256 + 33

from bs4 import BeautifulSoup
import requests
import ipaddress
link = "https://wiki.metakgp.org/w/IP_allocation_of_halls"
response = requests.get(link)
html = response.content
source = BeautifulSoup(html, "lxml")
trs = source.findAll("tr")
ip_to_hall = ['-']*(256*256)
for tr in trs:
    try:
        if len(tr.findAll("td")) != 3:
            continue
        tds = tr.findAll("td")
        addrs = tds[0].text.strip().split('.')
        place = tds[1].text.strip()
        if (len(addrs) == 4):
            ip_to_hall[int(addrs[1])*256 + int(addrs[2])] = place
            # print (addrs[1], int(addrs[1]), addrs[2], int(addrs[2]), int(addrs[1])*256 + int(addrs[2]))
        if (len(addrs) == 3):
            for ips in range(0, 256):
                ip_to_hall[int(addrs[1])*256 + ips] = place
    except Exception as e:
        print (e, tr)

# takes address as string like 10.117.31.15 and returns the hall
def probe(addr):
    addrs = addr.split('.')
    if (len(addrs) != 4):
        return "probe: ERROR! The given address format is incorrect"
    hash_ = int(addrs[1])*256 + int(addrs[2])
    if (ip_to_hall[hash_] != "-"):
        return ip_to_hall[hash_]
    else:
        i = hash_
        j = hash_
        # extrapolating backward and forward
        while i >=0 or j <= 65535:# (256*256 - 1)
            if (i >=1):
                i -= 1
                if (ip_to_hall[i] != "-"):
                    return ip_to_hall[i]
            if (j <= 65534):# (256*256 - 1 - 1)
                j += 1
                if (ip_to_hall[j] != "-"):
                    return ip_to_hall[j]
    return "probe: ERROR! We shouldn't reach here!"
