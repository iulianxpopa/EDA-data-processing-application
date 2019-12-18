import json

def change(type, name, psw):

    file = "WPASupplicantConfigs.json"
    #f = open("/etc/wpa_supplicant/wpa_supplicant.conf", "w")
    f = open("wpa_supplicant.conf", "w")

    with open(file) as configFile:
        try:
            data = json.load(configFile)
        except ValueError:
            print('wrong JSON')


    text = data[type]
    text = text.replace("__SSID__", name)
    text = text.replace("__PSK__", psw)

    f.write(text)
    f.close()

with open("NetworkConfig.json") as cfgFile:
    param = json.load(cfgFile)
    change(param["security"], param["ssid"], param["password"])

