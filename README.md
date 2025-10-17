# Unreliable PC Power Remote 🚀
# DOES NOT REQUIRE PORT FORWARDING 🥳
### secret message: still require port-forwarding for the HTTP/S WebServer to be accessible outside your network, or use some kind of tunneling service like the lightweight and low latency Tailscale 🤯
#### A stylish and secure PHP web panel designed to remotely power on your PC via an ESP32/Raspberry Pi. It features a stunning dark-mode, glassmorphism UI with exaggerated, interactive animations for a uniquely satisfying user experience.

<br>

## ✨ Features

* 🔒 **Secure Login System:** Protects the control panel with a PHP session-based username and password system. Passwords are securely hashed.
* 🎨 **Stunning Glassmorphism UI:** A modern, beautiful interface that looks great on any device.
* 💥 **Exaggerated Animations:**
    * **Rocket Launch:** Clicking the power button launches a rocket with a dynamic smoke trail!
    * **Interactive Elements:** Custom hover, click, and standby animations on all interactive elements.
    * **Animated Alerts:** Uses SweetAlert2 for beautiful, non-intrusive feedback.
* 🌐 **ThingSpeak Integration:** Uses the ThingSpeak IoT platform as a reliable bridge between the web panel and the hardware.
* 🔧 **Easy Configuration:** Sensitive details like API keys and login credentials are kept in a separate `config.php` file for easy setup and better security.
* 📱 **Responsive Design:** The interface is fully responsive and works great on desktops, tablets, and mobile phones.

## ⚙️ How It Works

The system architecture is simple and robust, using a cloud service to decouple the web interface from the hardware.

1.  **User Interaction:** You log in and press the "launch" button on the PHP web panel.
2.  **API Call:** The PHP server sends a secure POST request to the ThingSpeak API, updating a specific field in your channel to `1`.
3.  **Microcontroller Polling:** An ESP32 or similar microcontroller, connected to your PC's motherboard, is constantly polling this ThingSpeak field.
4.  **Action Triggered:** When the microcontroller detects the field value has changed to `1`, it briefly connects two GPIO pins. These pins are wired to your PC's power switch headers, simulating a physical button press.
5.  **Signal Reset:** The microcontroller then immediately sends another API call to ThingSpeak to reset the field value to `0`, preventing accidental re-triggers.

**Flow Diagram:**
`[You] ➡️ [Remote Web Panel] ➡️ [ThingSpeak API] ➡️ [ESP32 Microcontroller] ➡️ [PC Power Switch]`

---

## 🛠️ Technology Stack

* **Frontend:** HTML5, CSS3 (with advanced Keyframe animations), JavaScript, [SweetAlert2](https://sweetalert2.github.io/)
* **Backend:** PHP (with the cURL extension)
* **IoT Platform:** [ThingSpeak](https://thingspeak.com/)
* **Hardware:** ESP32 (recommended) or Raspberry Pi
* **Firmware:** MicroPython

---

## 📋 Prerequisites

### Hardware
* A web server that can run PHP (e.g., a Raspberry Pi, a VPS, or a shared hosting plan).
* An ESP32 development board (recommended for its low power consumption).
* Jumper wires (female-to-female).
* The PC you wish to control.

### Software
* A ThingSpeak account with a new Channel created. You will need the **Channel ID**, **Write API Key**, and **Read API Key**.
* PHP installed on your web server with the `cURL` extension enabled.
* A MicroPython development environment like [Thonny](https://thonny.org/) for the ESP32.

---

## 🚀 Installation & Setup

This is a two-part setup: first the web panel, then the microcontroller.

### Part 1: Web Panel Setup

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/unreliablecode/Unreliable-Power-Remote.git](https://github.com/unreliablecode/Unreliable-Power-Remote.git)
    ```

2.  **Deploy to Server:** Upload the `index.php`, `config.php`, and `logout.php` files to a directory on your web server.

3.  **Configure `config.php`:** This is the most important step.
    * **`THINGSPEAK_WRITE_KEY`**: Paste your ThingSpeak Channel's **Write API Key**.
    * **`USERNAME`**: Change the default username if you wish.
    * **`PASSWORD_HASH`**: **Do not store a plaintext password!** To generate a new secure hash for your chosen password, create a temporary PHP file with the following content, run it once, and copy the output into `config.php`:
        ```php
        <?php
        echo password_hash("YourNewPasswordHere", PASSWORD_DEFAULT);
        ?>
        ```

### Part 2: Microcontroller (ESP32) Setup



1.  **Wiring:**
    * **SAFETY FIRST:** Disconnect your PC from wall power before opening the case.
    * Locate the front panel headers on your motherboard (often labeled `F_PANEL` or `JFP1`).
    * Identify the pins for the power switch (`POWER SW`, `PWR_BTN`, etc.). They are not polarized.
    * Connect one jumper wire from a GPIO pin on your ESP32 (e.g., `GPIO4`) to one of the `POWER SW` pins.
    * Connect another jumper wire from a `GND` (Ground) pin on your ESP32 to the other `POWER SW` pin.

2.  **Flash MicroPython:** Follow a standard guide to flash the latest version of MicroPython onto your ESP32 board.

3.  **Configure the Code:** Create a `config.py` file on the ESP32 with your credentials.
    ```python
    # config.py for ESP32
    WIFI_SSID = "YourWiFiNetworkName"
    WIFI_PASS = "YourWiFiPassword"

    CHANNEL_ID = "YourThingSpeakChannelID"
    READ_API_KEY = "YourThingSpeakReadAPIKey"
    WRITE_API_KEY = "YourThingSpeakWriteAPIKey"
    ```

4.  **Upload Code:** Upload the provided `main.py` and your newly created `config.py` to the root directory of the ESP32 using Thonny.

5.  **Power & Run:** Power your ESP32 (e.g., via a USB phone charger). It will automatically connect to your WiFi and start listening for commands from ThingSpeak. The script is designed to run forever and automatically recover from network errors.

---

## 💡 Usage

1.  Navigate to the URL where you uploaded the `index.php` file.
2.  Log in with the credentials you configured.
3.  Click the giant, glowing power button.
4.  Watch the rocket launch and your PC turn on!

---

## 🔒 Security Considerations

* **Password Hashing:** This project uses `password_hash()` and `password_verify()`, which are the current PHP standards for secure password management.
* **Server Hardening:** Do not expose this web panel to the public internet unless your server is properly secured (e.g., using HTTPS, a firewall, and other best practices).
* **API Keys:** Treat your ThingSpeak API keys like passwords. Do not share them publicly.

---

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

* **SweetAlert2** for the beautiful and responsive alerts.
* **Google Fonts** for the modern 'Poppins' font.
* The web development community for pioneering the stunning glassmorphism design trend.
