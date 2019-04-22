robo-weather
============

This is a simple script that can be used to show the weather on a `Pimoroni
Scroll pHAT HD <https://shop.pimoroni.com/products/scroll-phat-hd>`_.

This also works with a `Scroll Bot <https://shop.pimoroni.com/products/scroll-bot-pi-zero-w-project-kit>`_.

Configuration
-------------

To configure this, edit the robo-weather.py script and change the
WEATHER_LOCATION to your 4 letter stationIdentifier from the
https://api.weather.gov/ api. For example,
https://api.weather.gov/stations?state=CO will list all the stations for Colorado.
See the `National Weather Service's API Specifications <https://www.weather.gov/documentation/services-web-api>`_.

Installation
------------

1. You'll need to install the `scroll-phat-hd <https://github.com/pimoroni/scroll-phat-hd>`_ library on your system.
2. Configure the robo-weather.py with your local weather stationIdentifier.
3. Copy robo-weather.py file to /usr/bin/robo-weather.py

.. code-block:: bash

    sudo cp robo-weather.py /usr/bin/robo-weather.py

4. Copy robo-weather.service file to /etc/systemd/system/robo-weather.service

.. code-block:: bash

    sudo cp robo-weather.service /etc/systemd/system/robo-weather.service

5. Enable the service and start it

.. code-block:: bash

    sudo systemd enable robo-weather
    sudo systemd start robo-weather
