#!/usr/bin/env python
#
#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#
#   Copyright 2019 Alex Schultz <aschultz@next-development.com>
#
import json
import scrollphathd
import signal
import sys
import time
import urllib2

from scrollphathd.fonts import font3x5

# API reference: https://www.weather.gov/documentation/services-web-api
WEATHER_REFRESH_RATE=180
WEATHER_LOCATION='KBKF'
WEATHER_URL_TEMPLATE='https://api.weather.gov/stations/{location}/' \
                     'observations/latest?require_qc=true'


class Weather():
    def __init__(self, location=None):
        self.location = location
        self.current_weather = {}
        self.headers = {'User-Agent': 'Robo-Weather 0.0.2',
                        'Accept': 'application/geo+json'}

    def get_temp_in_c(self):
        return self.current_weather.get('value', 'bzzz')

    def get_temp_in_f(self):
        if not self.current_weather.get('value', False):
           return 'bzzz'

        val = 9.0 / 5.0 * self.current_weather['value'] + 32
        return "{0:.1f}".format(val)

    def get_weather(self):
        url = WEATHER_URL_TEMPLATE.format(location=self.location)
        req = urllib2.Request(url, None, self.headers)
        try:
            resp = urllib2.urlopen(req)
            data = json.loads(resp.read())
            resp.close()
            self.current_weather = data.get('properties',
                                            {}).get('temperature',
                                                    {})
        except Exception as e:
            print('exception querying weather, {}'.format(e))

    def weather_string(self):
        weather_string = "{}".format(self.get_temp_in_f())
        return weather_string


class RoboWeatherDisplay():
    def __init__(self, rotate=True, font=font3x5):
        if rotate:
            scrollphathd.rotate(180)
        self.font = font
        self.brightness = 1.0
        scrollphathd.write_string('Starting Weather....',
                                  x=1,
                                  y=1,
                                  font=self.font,
                                  brightness=self.brightness)
        for i in range(0,75):
            scrollphathd.show()
            scrollphathd.scroll()
            time.sleep(0.05)

        scrollphathd.clear()

    def show_weather(self, weather):
        while True:
            #print 'Brightness is...{}'.format(self.brightness)
            if self.brightness <= 0.1:
                self.brightness = 1.0
                weather.get_weather()
                scrollphathd.clear()

            scrollphathd.write_string(weather.weather_string(),
                                      x=1,
                                      y=1,
                                      font=self.font,
                                      brightness=self.brightness)
            scrollphathd.show()
            time.sleep(WEATHER_REFRESH_RATE/10)
            self.brightness = self.brightness - 0.1

    def cleanup(self):
        scrollphathd.clear()
        sys.exit(0)


if __name__ == '__main__':
    w = Weather(location=WEATHER_LOCATION)
    w.get_weather()

    display = RoboWeatherDisplay()
    signal.signal(signal.SIGTERM, display.cleanup)
    display.show_weather(w)

