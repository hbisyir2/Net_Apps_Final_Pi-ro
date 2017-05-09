# Net_Apps_Final_Pi-ro
Fire alarm live temperature map system using several Raspberry Pis, thermometers, and maps


-- For setting up thermometer Pis --
Use this tutorial and follow the steps on your pi

https://cdn-learn.adafruit.com/downloads/pdf/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing.pdf

-- map pi --
Uses i2c to update seven segment displays, must enable on Raspberry Pi configurations
Uses Adafruit library to update displays

-- server pi --
Uses socket communications and JSON library to compile and organize information

Pi-ro
Updates several three color LEDs and seven segment displays on a physical map for use in a fire.  A user will be able to look at the map, see areas of high heat, and plan their exit route accordingly. LEDs will light up green, yellow, or red representing the severity of heat levels in a given area.  The seven segment displays will update every second to show how long it has been since the LED was last updated.  In case a thermometer breaks and stops sending temperature information, a user can see that an LED has not been update in x amount of seconds and alter their exit route accordingly.

Usage:
python2 mappi_comm.py -p <port_to_server>
python3.4 temperature_1.py -i <server_ip> -p <port_to_server>
python3.4 temperature_2.py -i <server_ip> -p <port_to_server>
python3.4 serverpi_thread.py -i <map_ip> -p1 <port_to_thermometer_1> -p2 <port_to_thermometer_2> -p3 <port_to_map>
