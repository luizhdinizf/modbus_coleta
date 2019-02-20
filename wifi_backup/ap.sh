#!/bin/bash
sudo cp /home/pi/fca-iot/utils/wifi_backup/interfaces.d/interfaces /etc/network/interfaces.d/interfaces 
sudo cp /home/pi/fca-iot/utils/wifi_backup/dhcpcd.conf.ap /etc/dhcpcd.conf
sudo cp /home/pi/fca-iot/utils/wifi_backup/dnsmasq.conf.ap /etc/dnsmasq.conf
sudo cp /home/pi/fca-iot/utils/wifi_backup/hostapd.conf.ap /etc/hostapd/hostapd.conf
sudo cp /home/pi/fca-iot/utils/wifi_backup/interfaces.ap /etc/network/interfaces 
sudo cp /home/pi/fca-iot/utils/wifi_backup/hostapd.ap /etc/default/hostapd
