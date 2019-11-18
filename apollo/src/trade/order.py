import requests
import os
import logging

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p',
    level=logging.INFO,
    #filename='log.txt'
)

class Order():

    def __init__(self, inv_instrument, take_profit):
        """Inicializa nuestra red.

        Args:
            inv_instrument (str): instrument's name
            take_profit (float): take profit price
        """
        self.auth_token = os.environ['token'] #token de autenticación
        self.head = {'Authorization': 'Bearer ' + self.auth_token} # header
        self.url = os.environ['trading_url'] # URL de broker
        self.tradeID = 0
        self.take_profit = take_profit
        #self.stop_loss = stop_loss
        self.market_price = 0
        self.inv_instrument = inv_instrument

    def make_market_order(self, units):
        data = {
            "order" :{
            	"type": "MARKET",
            	"instrument": self.inv_instrument,
            	"units": str(units),
                "takeProfitOnFill":{
                    "price": str(self.take_profit)
                },
                #"stopLossOnFill":{
                    #"price": str(self.stop_loss)
                #}
            }
        }


        url = self.url + 'orders'
        #try:
        response = requests.post(url, json=data, headers=self.head)
        print(f'Response code for Order sent:\n{response}')
        json_response = response.json()
        print(f'Content of response:\n{json_response}')
        self.tradeID = json_response['orderCreateTransaction']['id']
        #self.market_price = json_response['orderCreateTransaction']['price']
        #except requests.exceptions.RequestException as e:
            #logging.info(e)
            #sys.exit(1)

        return json_response


    def show_order(self):
        print(f"""\ntradeID: {self.tradeID}\
                  \nmarket_price: {self.market_price}\
                  \ntake_profit: {self.take_profit}""")

if __name__ == "__main__":
    new_order = Order('USD_JPY', '107.981')
    new_order.make_market_order('-1')