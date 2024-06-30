
import time                   # Allows use of time.sleep() for delays
from mqtt import MQTTClient   # For use of MQTT protocol to talk to Adafruit IO
import machine                # Interfaces with hardware components
from machine import Pin       # Define pin
import keys                   # Contain all keys used here
import wifiConnection         # Contains functions to connect/disconnect from WiFi 
from rotary_irq_rp2 import RotaryIRQ # Import Rotary functions
from machine import I2C, Pin         # Import information from I2C Pin
from ssd1306 import SSD1306_I2C      # Import Screen functionalities
import dht                           # Import Thermometer and Humidity sensor funcions
# from machine import Pin, Timer

# For testning connectivity with led
led = Pin("LED", Pin.OUT)   # led pin initialization for Raspberry Pi Pico W

# Establish connection for LED, Temp sensor and Rotary encoder
i2c = I2C(0,sda=Pin(16), scl=Pin(17))
display = SSD1306_I2C(128, 32, i2c)
tempSensor = dht.DHT11(machine.Pin(18))

# Set values for rotary encoder
r = RotaryIRQ(pin_num_clk=13,
              pin_num_dt=14,
              min_val=5, # Min value needs to be < 1 to never divide by 0 in calc
              max_val=50,
              incr=5,
              reverse=False,
              range_mode=RotaryIRQ.RANGE_BOUNDED
              )

# push_button = Pin(15, Pin.IN)

# Callback Function to respond to messages from Adafruit IO
def sub_cb(topic, msg):          # sub_cb means "callback subroutine"
    print((topic, msg))          # Outputs the message that was received. Debugging use.
    if msg == b"ON":             # If message says "ON" ...
        led.on()                 # ... then LED on
    elif msg == b"OFF":          # If message says "OFF" ...
        led.off()                # ... then LED off
    else:                        # If any other message is received ...
        print("Unknown message") # ... do nothing but output that it happened.

# Mesure temperature and humidity with sensor
def read_temp():
    try:
        tempSensor.measure()  # Trigger the sensor to measure temperature and humidity
        temperature = tempSensor.temperature()  # Get the temperature in Celsius
        humidity = tempSensor.humidity()  # Get the humidity percentage
        # print(temperature, humidity)
        return temperature, humidity
    
    except OSError:
        print('Failed to read sensor:')
        return None, None
    
temprature,humidity = read_temp()


# Recomend proofint time depending on temperature whitout regard to yeast amount
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

def calculate(T, Y):
    Y = Y / 100  # Divide rotary encoder value lowest is 1 highest is 50 so make it into decimals for easier calcs
    calc_min  = T / (Y * 2)   # The formula T / (Y / 100 * 2) to calc minutes
    calc_result = calc_min / 60 # convert to hours
    return round(calc_result)

T = adjusted_val # The time based on temperature
Y = r.value() # The rotary encoder value for setting yeast ammount
calc_result = calculate(T, Y)

# Display function show selected yeast and temp/humid
def update_display(r, display):
    temp_val,humidity_val = read_temp() #Get temperature and humidity from sensor
    display.fill(0)
    rot_val = r.value()
    dry_val = round(rot_val / 4.2) # simple yeast cube to dry yeast conversion(yeast cube expected in calcs this is only for user conveniance)
    display.text("Temp {}C H {}%" .format(temp_val, humidity_val) , 2, 8) # Display on the screen, first row
    display.text("Cube {}g Dry {}g" .format(rot_val, dry_val) , 2, 20) # Display on the screen, secound row
    display.show()  # Refresh the display

update_display(r, display)

# Send values to Adafruit
def send_values():

    temp_val,humidity_val = read_temp() #Get temperature and humidity from sensor

    #Send values to Adafruit IO, values sent: Temperature, Humidity and Proof Time
    try:
        client.publish(topic=keys.AIO_TEMPERATURE_FEED, msg=str(temp_val))
        client.publish(topic=keys.AIO_HUMIDITY_FEED, msg=str(humidity_val))
        client.publish(topic=keys.AIO_RECOMMEND_FEED, msg=str(calc_result))
        print("DONE")
    except Exception as e:
        print("FAILED")
    finally:
        print("Publishing: {0} temp /{1} humid /{2} h result /{3} yeast... ".format(temp_val, humidity_val, calc_result, Y), end='')

# Try WiFi Connection
try:
    ip = wifiConnection.connect()
except KeyboardInterrupt:
    print("Keyboard interrupt")

# Use the MQTT protocol to connect to Adafruit IO
client = MQTTClient(keys.AIO_CLIENT_ID, keys.AIO_SERVER, keys.AIO_PORT, keys.AIO_USER, keys.AIO_KEY)

# Subscribed messages will be delivered to this callback
client.set_callback(sub_cb)
client.connect()
client.subscribe(keys.AIO_LIGHTS_FEED)
print("Connected to %s, subscribed to %s topic" % (keys.AIO_SERVER, keys.AIO_LIGHTS_FEED))


try:                      # Code between try: and finally: may cause an error
                          # so ensure the client disconnects the server if
                          # that happens.
    while 1:              # Repeat this loop forever

        if time.time() % 20 == 0:  # A separate timer to send data as to not get throtteled 
            send_values()     # Sen values in loop

        calc_result = calculate(T, Y) # 
        Y = r.value() #Update the Rotary value 
        update_display(r, display) # Update display in loop
        client.check_msg() # Action a message if one is received. Non-blocking.
        time.sleep(1) # Timer for loop kept low so as to not particurally affect rotary feel

finally:                  # If an exception is thrown ...
    client.disconnect()   # ... disconnect the client and clean up.
    client = None
    wifiConnection.disconnect()
    print("Disconnected from Adafruit IO.")


