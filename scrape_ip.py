# This uses second and third placeholder in the address for hashing
# That is in 10.102.33.44 it uses 102 and 33 for hashing
# into base 256, i.e. 102*256 + 33

from bs4 import BeautifulSoup
import requests
import ipaddress
from datetime import datetime
import pickle

class ScrapeIP:
    ip_to_hall = ['-']*(256*256)
    data_list = []
    def __init__(self, fromFile):
        if (not fromFile):
            link = "https://wiki.metakgp.org/w/IP_allocation_of_halls"
            response = requests.get(link)
            html = response.content
            source = BeautifulSoup(html, "lxml")
            trs = source.findAll("tr")
            for tr in trs:
                try:
                    if len(tr.findAll("td")) != 3:
                        continue
                    tds = tr.findAll("td")
                    addrs = tds[0].text.strip().split('.')
                    place = tds[1].text.strip()
                    if (len(addrs) == 4):
                        self.ip_to_hall[int(addrs[1])*256 + int(addrs[2])] = place
                        # print (addrs[1], int(addrs[1]), addrs[2], int(addrs[2]), int(addrs[1])*256 + int(addrs[2]))
                    if (len(addrs) == 3):
                        for ips in range(0, 256):
                            self.ip_to_hall[int(addrs[1])*256 + ips] = place
                except Exception as e:
                    print (e, tr)
            with open("backup_ip.txt", "wb") as fp:   #Pickling
                pickle.dump(self.ip_to_hall, fp)
        else:
            with open("backup_ip.txt", "rb") as fp:   # Unpickling
                self.ip_to_hall = pickle.load(fp)
    # takes address as string like 10.117.31.15 and returns the hall
    def probe(self, addr):
        addrs = addr.split('.')
        if (len(addrs) != 4):
            return "probe: ERROR! The given address format is incorrect"
        hash_ = int(addrs[1])*256 + int(addrs[2])
        if (self.ip_to_hall[hash_] != "-"):
            return self.ip_to_hall[hash_]
        else:
            i = hash_
            j = hash_
            # extrapolating backward and forward
            while i >=0 or j <= 65535:# (256*256 - 1)
                if (i >=1):
                    i -= 1
                    if (self.ip_to_hall[i] != "-"):
                        return self.ip_to_hall[i]
                if (j <= 65534):# (256*256 - 1 - 1)
                    j += 1
                    if (self.ip_to_hall[j] != "-"):
                        return self.ip_to_hall[j]
        return "probe: ERROR! We shouldn't reach here!"
    def parse(self, file_name):
        f = open(file_name, "r")
        data = f.readlines()
        data_list = []
        for data_entry in data:
            try:
                data_split = data_entry.split(" ")
                sub_dict = {}
                sub_dict["time"] = datetime.strptime(data_split[0] + " " + data_split[1], '%Y-%m-%d %H:%M:%S')
                sub_dict["hall"] = self.probe(data_split[2])
                sub_dict["term"] = data_entry[len(data_split[0]) + len(data_split[1]) + len(data_split[2]) + 3:].strip()[1:-1]
                data_list.append(sub_dict)
            except Exception as e:
                print (e, data_entry)
        return data_list

a = ScrapeIP(fromFile=False)

tmp = a.parse("data/2017-04-08 16:00")

hall_count = {}
for a in tmp:
    if a["hall"] in hall_count:
        hall_count[a["hall"]] += 1
    else:
        hall_count[a["hall"]] = 1
