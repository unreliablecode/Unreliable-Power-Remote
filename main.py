# main.py

import network
import urequests
import time
from machine import Pin
import config # Import our credentials

# --- Constants ---
PC_POWER_PIN = 4 # The GPIO pin connected to the PC's POWER SW header
POLL_INTERVAL_S = 15 # Check ThingSpeak every 15 seconds (free limit)

# ThingSpeak URLs
READ_URL = f"https://api.thingspeak.com/channels/{config.CHANNEL_ID}/fields/1/last.json?api_key={config.READ_API_KEY}"
WRITE_URL = f"https://api.thingspeak.com/update?api_key={config.WRITE_API_KEY}"

# --- Pin Setup ---
# Set pin as an output, and set it high initially.
# Pulling it LOW will simulate the button press.
power_pin = Pin(PC_POWER_PIN, Pin.OUT)
power_pin.value(1)

# --- Functions ---

def check_wifi_connection():
    """Check if WiFi is still connected, reconnect if necessary."""
    wlan = network.WLAN(network.STA_IF)
    if not wlan.isconnected():
        print("WiFi connection lost. Reconnecting...")
        return connect_wifi()
    return True

def connect_wifi():
    """Connects the ESP32 to WiFi with better error handling."""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    # Disconnect first to clear any previous connection
    wlan.disconnect()
    time.sleep(1)
    
    if not wlan.isconnected():
        print(f"Connecting to network '{config.WIFI_SSID}'...")
        wlan.connect(config.WIFI_SSID, config.WIFI_PASS)
        
        # Wait for connection with better status reporting
        max_wait = 20
        while max_wait > 0:
            status = wlan.status()
            status_messages = {
                1000: "STATUS_IDLE",
                1001: "STATUS_CONNECTING",
                202: "STATUS_WRONG_PASSWORD",
                201: "STATUS_NO_AP_FOUND",
                1010: "STATUS_GOT_IP",
                204: "STATUS_CONNECT_FAIL"
            }
            print(f"WiFi status: {status} ({status_messages.get(status, 'UNKNOWN')})")
            
            if wlan.isconnected():
                break
                
            max_wait -= 1
            time.sleep(1)

    if wlan.isconnected():
        print("✅ WiFi Connected!")
        print('IP Address:', wlan.ifconfig()[0])
        return True
    else:
        print("❌ WiFi Connection Failed!")
        final_status = wlan.status()
        print(f"Final connection status: {final_status}")
        
        # Provide helpful error messages
        if final_status == 201:
            print("Error: Network not found. Check SSID.")
        elif final_status == 202:
            print("Error: Wrong password.")
        elif final_status == 204:
            print("Error: Connection failed. Check signal strength.")
            
        return False

def toggle_pc_power():
    """Simulates a power button press."""
    print("Toggling PC power...")
    power_pin.value(0) # Pull pin LOW
    time.sleep(0.5)    # Hold for 500ms
    power_pin.value(1) # Release by pulling HIGH
    print("Toggle signal sent.")

def reset_thingspeak_command():
    """Resets the command field to 0 to prevent re-triggering."""
    print("Resetting ThingSpeak command field to 0...")
    reset_url = f"{WRITE_URL}&field1=0"
    try:
        response = urequests.get(reset_url)
        if response.status_code == 200:
            print("ThingSpeak command field has been reset.")
        else:
            print(f"Error resetting command field. Status: {response.status_code}")
        response.close()
    except Exception as e:
        print(f"Failed to reset ThingSpeak command: {e}")

# --- Main Loop ---
# --- Main Loop ---
if connect_wifi():
    while True:
        try:
            # Check WiFi connection before making request
            if not check_wifi_connection():
                print("Skipping ThingSpeak check due to WiFi issues...")
                time.sleep(POLL_INTERVAL_S)
                continue
                
            print(f"\nChecking ThingSpeak... ({time.ticks_ms()})")
            
            # Get the last command from ThingSpeak
            response = urequests.get(READ_URL, timeout=10)
            
            if response.status_code == 200:
                json_data = response.json()
                command = json_data.get('field1')
                print(f"Received command: '{command}'")

                if command == '1':
                    toggle_pc_power()
                    reset_thingspeak_command()
            else:
                print(f"Error reading from ThingSpeak. Status: {response.status_code}")

            response.close()

        except OSError as e:
            print(f"Network error: {e}")
            # Force WiFi reconnect on network errors
            connect_wifi()
        except Exception as e:
            print(f"An error occurred: {e}")

        time.sleep(POLL_INTERVAL_S)
