
from bs4 import BeautifulSoup
import requests
import json
import fire
import os
"""

"""
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
}
clear_config = True


class NodeInfo:
    def __init__(self, remarks='',
                 id='',
                 server='',
                 server_port=0,
                 server_udp_port=0,
                 password='',
                 method='',
                 protocol='',
                 protocolparam='',
                 obfs='plain',
                 obfsparam='',
                 remarks_base64='',
                 group='',
                 enable=True,
                 udp_over_tcp=False):
        self.remarks = remarks
        self.id = id
        self.server = server
        self.server_port = server_port
        self.server_udp_port = server_udp_port
        self.password = password
        self.method = method
        self.protocol = protocol
        self.protocolparam = protocolparam
        self.obfs = obfs
        self.obfsparam = obfsparam
        self.remarks_base64 = remarks_base64
        self.group = group
        self.enable = enable
        self.udp_over_tcp = udp_over_tcp


def fill_config(json_path):
    if not os.path.exists(json_path):
        return
    url = ''
    wb_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    contents = soup.select('div.hover-text > h4')

    with open(json_path, 'r') as f:
        json_content = json.load(f)
        # print(content)
        # print(len(content['configs']))
        # print(content['configs'][0])
        # print(content['configs'][1])
    if clear_config:
        json_content['configs'].clear()
        # print(len(content['configs']))

    for i in range(0, len(contents), 5):
        server = contents[i].get_text().split(':')[1].strip()
        server_port = contents[i + 1].get_text().split(':')[1].strip()
        password = contents[i + 2].get_text().split(':')[1].strip()
        method = contents[i + 3].get_text().split(':')[1].strip()
        if len(server) == 0 or len(server_port) == 0 or len(password) == 0 or len(method) == 0:
            pass
        else:
            # print(contents[i].get_text().split(':')[1].strip(), contents[i + 1].get_text().split(':')[1].strip(),
            #       contents[i + 2].get_text().split(':')[1].strip(), contents[i + 3].get_text().split(':')[1].strip())
            json_content['configs'].append(NodeInfo(server=server, server_port=server_port, password=password,
                                                    method=method).__dict__)
    with open(json_path, 'w') as f:
        json.dump(json_content, f)


if __name__ == '__main__':
    fire.Fire()




