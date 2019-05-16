import requests
from prometheus_client import Metric

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/70.0.3538.77 Chrome/70.0.3538.77 Safari/537.36'}
takealot_api = 'https://api.takealot.com/rest/v-1-7-0/product-details/{}?platform=desktop'

class Exporter(object):
    def __init__(self, plids):
        self.plids = plids

    def collect(self):
        for plid in self.plids:
            try:    
                print("Collect Request - {}".format(plid))
                request_url = takealot_api.format(plid)
                result = requests.get(request_url, headers=headers).json()

                product_data = result['event_data']["documents"]['product']
                product_title = result['core']['title']

                # Current price
                metric = Metric('product_data_purchase_price', 'Product Data - {}'.format(plid), 'gauge')
                metric.add_sample('product_data_purchase_price', labels={'title': product_title, 'plid': plid},
                                  value=product_data['purchase_price'])
                yield metric

                # Original price
                metric = Metric('product_data_original_price', 'Product Data - {}'.format(plid), 'gauge')
                metric.add_sample('product_data_original_price', labels={'title': product_title, 'plid': plid},
                                  value=product_data['original_price'])
                yield metric

                # Stock check
                metric = Metric('product_data_in_stock', 'Product Data - {}'.format(plid), 'gauge')
                metric.add_sample('product_data_in_stock', labels={'title': product_title, 'plid': plid},
                                  value=product_data['in_stock'])
                yield metric
            except KeyError as e:
                print(e)

