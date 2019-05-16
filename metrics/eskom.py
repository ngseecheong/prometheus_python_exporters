import requests
from prometheus_client import Metric

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/70.0.3538.77 Chrome/70.0.3538.77 Safari/537.36'}
loadshedding_eskom_url = 'http://loadshedding.eskom.co.za/LoadShedding/GetStatus'


class Exporter(object):

    def collect(self):
        print("Collect Eskom Request")
        request_url = loadshedding_eskom_url
        result = requests.get(request_url, headers=headers)

        if result.status_code != 200:
            print("Failed to collect data")
        else:
            metric = Metric('eskom_loadshedding_status', 'Eskom', 'gauge')
            metric.add_sample('eskom_loadshedding_status', labels={'title': 'loadshedding'}, value=int(result.text))
            yield metric
