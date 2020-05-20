from dnacentersdk import DNACenterAPI, ApiError
from pprint import pprint
from configparser import ConfigParser

config = ConfigParser() # using a .ini file to hide my personal home meraki api key :)
ini = config.read('config.ini') # reading ini file
username = str(config.get('config', 'username')) # openting the .ini file to get the api key 
password = str(config.get('config', 'password'))
base_url = str(config.get('config', 'base_url'))
def main():
    try:
        api = DNACenterAPI(username=username, password=password, base_url=base_url, verify=False)

        get_discovery = api.clients.get_overall_client_health()
        get_site = api.sites.get_site_count()
        print (get_site)

        get_device_count = api.devices.get_device_config_for_all_devices()
        get_device = api.devices.retrieve_all_network_devices()
        print(get_device_count)
        get_device_list = api.devices.get_device_list()
        pprint (get_device_list)
    except ApiError as e:
        print(e)
get_device_list
if __name__ == "__main__":
    main()

# use help(api.devices)