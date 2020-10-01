---
layout: default
title: Tonight's Conditions
nav_order: 4
---

## Two-Day Forecast

<img src="https://www.cleardarksky.com/c/Clevelandcsk.gif?c=2761241">

For a full key, refer to [the official Clear Dark Sky site](https://www.cleardarksky.com/c/Clevelandkey.html). Put simply, the best observation times are when everything except the temperature is dark blue, which reflects good visibility, and when the temperature is orange, which reflects a comfortable temperature. The observatory dome is not heated, so dress appropriately for the weather.

## Tonight's Objects

This gives a list of planets and bright stars which are in a good observing position tonight. It gives the current position of the objects in Hour Angle and Declination, so that finding the object on the telescope is simple, and the times the object rises above and sets below 30 degrees above the horizon. 30 degrees is used instead of the horizon to account for light pollution, atmospheric distortion, and other effects which make sighting an object lower on the sky difficult.

For times, a 24-hour clock is used: for example, 8 PM will be listed as 20.

Due to the telescope's age, the measures on the telescope are off slightly. Once the telescope is pointed in the right area, use the finder telescope to get the exact position.

### Bright Stars Visible
<table>
  {% for row in site.data.nightstars %}
    {% if forloop.first %}
    <tr>
      {% for pair in row %}
        <th>{{ pair[0] }}</th>
      {% endfor %}
    </tr>
    {% endif %}

    {% tablerow pair in row %}
      {{ pair[1] }}
    {% endtablerow %}
  {% endfor %}
</table>

### Planets (or the Moon) Visible
<table>
  {% for row in site.data.nightplanets %}
    {% if forloop.first %}
    <tr>
      {% for pair in row %}
        <th>{{ pair[0] }}</th>
      {% endfor %}
    </tr>
    {% endif %}

    {% tablerow pair in row %}
      {{ pair[1] }}
    {% endtablerow %}
  {% endfor %}
</table>