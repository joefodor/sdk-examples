from meraki_sdk.meraki_sdk_client import MerakiSdkClient 
from meraki_sdk.exceptions.api_exception import APIException
from meraki_sdk.models.blink_network_device_leds_model import BlinkNetworkDeviceLedsModel
from pprint import pprint
from configparser import ConfigParser

def main():
    config = ConfigParser() # using a .ini file to hide my personal home meraki api key :)
    ini = config.read('config.ini') # reading ini file
    x_cisco_meraki_api_key = str(config.get('config', 'api_key')) # opening the .ini file to get the api key 

    meraki = MerakiSdkClient(x_cisco_meraki_api_key) # the MerakiSdkClient is what setsup the API calls for you
    orgs = meraki.organizations.get_organizations() # setting up objerct to get all orginizations
    params = {} # creating empty dict
    params["organization_id"] = str(orgs[0]['id']) # adding my house org ID to the dict. The dict is required when sending params with the API
    nets = meraki.networks.get_organization_networks(params) # getting my orgs using params dict
    params["network_id"] = str(nets[0]['id']) # then adding the network id I pulled to params for later use

    # lets make my home equipment blink! This is an example from merakis quick start SDK
    blink = BlinkNetworkDeviceLedsModel()
    blink.duration = 40
    blink.period = 160
    blink.duty = 50

    x = meraki.devices.get_network_devices(params["network_id"])# Here I used devices.get_network_devices and used the network_id in params to pull them all down

    # we can see I have 3 meraki devices 
    pprint(x)

    # in order to make them blink we have to pass in another param that I added according to the doc
    params['blink_network_device_leds'] = blink

    try:
        # here we loop through each device getting the serial number and then running the blink_network_device_leds api.
        # for each device the serial number will get ovewritten in the params dict before running the API call.
        for i in x: 
            params['serial'] = i['serial']
            result = meraki.devices.blink_network_device_leds(params)
            print(result)
    except APIException as e:
        print(e)


    # simple way to use the SDK to get the ips of all the devices on the network
    ip = []
    devices = {}
    devices["network_id"] = str(nets[0]['id'])
    try:
        result = meraki.clients.get_network_clients(devices)
        for i in result:
            ip.append(i['ip'])
        pprint(result)
        print(ip)
    except APIException as e:
        print(e)
if __name__ == "__main__":
    main()