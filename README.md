# pyHelialux

Python library to control (and get information from) Juwel's Helialux Smart Controller.

## Suppored features
* Get current state of the controller
  * `currentProfile`
  * `currentWhite`
  * `currentBlue`
  * `currentGreen`
  * `currentRed`
  * `manualColorSimulationEanbled`
  * `manualDaytimeSimulationEnabled`
  * `deviceTime`
* Enable and disable manual color simulation
* Set the brightness of the channels manually

## Example code
```
import helialux
from time import sleep

c = helialux.Controller(url="http://192.168.1.100")
print(c.get_status())

print("Start manual")
c.start_manual_color_simulation(duration=5) # enable it for 5 minutes (defaults to 60)

sleep(2)
print("just blue")
c.set_manual_color(white=0, blue=100, green=0, red = 0)

sleep(2)
print("just white")
c.set_manual_color(white=100, blue=0, green=0, red = 0)

sleep(2)
print("off")
c.set_manual_color(white=0, blue=0, green=0, red = 0)
sleep(2)
print("Stop manual")
c.stop_manual_color_simulation()
```


[Buy me a coffee :)](https://paypal.me/MaartenHoogendoorn)
