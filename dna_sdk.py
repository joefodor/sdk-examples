from dnacentersdk import DNACenterAPI, ApiError
from pprint import pprint
from configparser import ConfigParser

config = ConfigParser() # using a .ini file to hide my personal home meraki api key :)
ini = config.read('config.ini') # reading ini file
username = str(config.get('config', 'username')) # opening the .ini file to get the api key 
password = str(config.get('config', 'password'))
base_url = str(config.get('config', 'base_url'))
def main():
    try:
        api = DNACenterAPI(username=username, password=password, base_url=base_url, verify=False) # This handles gather the token 

        get_discovery = api.clients.get_overall_client_health() # Getting overall client health
        client_count = get_discovery['response'][0]['scoreDetail'][0]['clientUniqueCount'] # parsing down to get global client count
    
        print (f"\nthe global client count is: {client_count}") # printing client count

        get_site = api.sites.get_site_count() # getting number of sites created
        print (f"The number of sites are: {get_site['response']}") # printing number of sites.
        
    except ApiError as e:
        print(e)

if __name__ == "__main__":
    main()

# use help(api.devices) or help(api.sites) to get all the possible methods. Also help(api.pnp)