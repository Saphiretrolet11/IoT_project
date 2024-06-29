Gustav Helgesson Liljedal gh222nq

# IoT_project
IoT_project

project overview
time to do

## Objective

## Materials

Materials used during the project:

| Component                                 | Description                            | Purchase Link                                                        | Price (SEK) |
|-------------------------------------------|----------------------------------------|----------------------------------------------------------------------|-----------|
| <img src="images/PICOWH.jpg" width="150"> | Raspberry Pi Pico WH                   | [Link](https://www.electrokit.com/raspberry-pi-pico-wh)                                  | 109   |
| <img src="images/DHT11.jpg" width="150">   | DHT11 Temperature and Humidity Sensor   | [Link](https://www.electrokit.com/produkt/digital-temperatur-och-fuktsensor-dht11/)                              | 49  |
| <img src="images/OLED.jpg" width="150">  | OLED LDC Displat                           | [Link](https://www.wish.com/product/5b960ef5f1220016bb853780)                               | 26         |
| <img src="images/ROTARY.jpg" width="150">    | Rotary Encoder   | [Link](https://www.az-delivery.de/en/products/drehimpulsgeber-modul)                                | 49         |
| <img src="images/BOARD.jpg" width="150">    | Breadboard    | [Link](https://www.electrokit.com/kopplingsdack-840-anslutningar)                                | 69         |
| <img src="images/M2M.jpg" width="150">    | Jumper Wire Male to Male    | [Link](https://www.electrokit.com/labbsladd-20-pin-15cm-hane/hane)                                | 29         |
| <img src="images/M2F.jpg" width="150">    | Jumper Wire Male to Female    | [Link](https://www.electrokit.com/labbsladd-20-pin-15cm-hona/hane)                                | 29         |
| <img src="images/USB.png"  height="150">    | USB-cable  Male to Female    | [Link](https://www.electrokit.com/usb-kabel-a-hane-micro-b-5p-hane-1.8m)                                | 39         |

## Computer Setup

## C
## Putting everything together

The DHT11 sensor is extended with M2F cables so it can be placed inside the proofing bowl while the rest of the device is outside protecting it form the damp and potential dough that could damage it

Rotary encoder extended with M2F cables due to the pins direction pointing the rotary towards the board and making it akward to use

## platform

## Code

- `boot.py` deals with Wi-Fi connection.
- `main.py` handles sensor readings, calculations and sends data
- `mqtt.py` 
- `wifiConnection` 
- `keys.py` mages credantials
- - `lib` mages credantials 

```
def calculate(T, Y):
    Y = Y / 100  # Divide rotary encoder value lowest is 1 highest is 50 so make it into decimals for easier calcs
    calc_min  = T / (Y * 2)   # The formula T / (Y / 100 * 2) to calc minutes
    calc_result = calc_min / 60 # convert to hours
    return round(calc_result)

T = adjusted_val # The time based on temperature
Y = r.value() # The rotary encoder value for setting yeast ammount
calc_result = calculate(T, Y)
```
qweqwe
```
def update_display(r, display):
    temp_val,humidity_val = read_temp() #Get temperature and humidity from sensor
    display.fill(0)
    rot_val = r.value()
    dry_val = round(rot_val / 4.2) # simple yeast cube to dry yeast conversion(yeast cube expected in calcs this is only for user conveniance)
    display.text("Temp {}C H {}%" .format(temp_val, humidity_val) , 2, 8) # Display on the screen, first row
    display.text("Cube {}g Dry {}g" .format(rot_val, dry_val) , 2, 20) # Display on the screen, secound row
    display.show()  # Refresh the display

update_display(r, display)
```
qweqweqw

```
def temp_time (temprature_min):
    if temprature_min < 0:
        value = 1
    elif 0 <= temprature_min < 8:
        value = 640
    elif 8 <= temprature_min < 14:
        value = 480
    elif 14 <= temprature_min < 20:
        value = 120
    elif 20 <= temprature_min < 30:
        value = 60
    else:
        value = 60
    return value

current_temp = temprature
# current_temp = 2
adjusted_val = temp_time(current_temp)
```
qweqwe

# Display function show selected yeast and temp/humid

## Transmitting data/connectivity

Wifi over lorawan
I decided to use wifi since i had no real usecase outide of my home kitchen and as wifi is readely avalible 
lorawan could be interesting to use as it requires less power and a much further range it could allow for some outdoor usage in perhaps a camping/mobile home senario if the device was protected in a case.

## Presenting data

## Finalizing the design
