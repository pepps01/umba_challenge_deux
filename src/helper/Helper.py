from flask import jsonify
import random
import requests
from dotenv import dotenv_values

class Helper:
    LOWEST_NUMBER =1000000000
    HIGHEST_NUMBER= 9999999999
    ENV_CONFIG = dotenv_values(".env")

    def response_message(self,result={}, message="Ok", status=200):
        return jsonify({
            "message": message,
            "result":result, 
            "status":status
        })
                               
    def get_user_id(self):
        from flask_jwt_extended import get_jwt_identity
        current_user =  get_jwt_identity()
        return current_user
    
    def error_messages(self):
        return 1
    
    def generate_account_number(self):
        random_number = random.randint(self.LOWEST_NUMBER, self.HIGHEST_NUMBER)
        return random_number
    
    def reveal_location(self, ip_address):
        try:
            url ="https://geo.ipify.org/api/v2/country?apiKey={api_key}&ipAddress={address}".format(api_key=self.ENV_CONFIG["IP_ADDRESS_SECRET_KEY"], address=ip_address)
            response =  requests.get(url)
            response_data= response.json()
            print("DATA",response_data)
            location= dict()
            location['user_ip'] = response_data["ip"]
            location['country'] = response_data["location"]['country']
            location['region'] = response_data["location"]['region']
            location['timezone'] = response_data["location"]['timezone']

            return location
        except ConnectionError:
            raise ConnectionError 
            
        

        