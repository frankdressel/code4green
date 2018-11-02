# code4green

This repository contains the source code and ideas about the _sleepy coders_ project _let me sleep_ at the [code4green](https://www.bmu.de/service/veranstaltungen/wettbewerbe/code4green/) hackathon.

## Development

### Languages

#### R

Download and install [R](https://cran.r-project.org/bin/windows/base/) and [RStudio](https://www.rstudio.com/products/rstudio/download/).

### VM

#### VirtualBox

Download and install [VirtualBox](https://www.virtualbox.org/).

## Simulation

The simulation will be done on a hexagonal grid. See [this article from redblobgames](https://www.redblobgames.com/grids/hexagons/).

The speed of sound (20°C, dry air) is approx. 1236 km/h (see [Wikipedia](https://de.wikipedia.org/wiki/Schallgeschwindigkeit)). This is neglectable against the speed of a car in the city (approx. 50 km/h). Thus, the time dependency of sound distribution is neglected in the simulation.

See [branch c4g](https://github.com/frankdressel/games/tree/c4g/patterns), in the file app/routes/application.js for a prototype.

### Data model

The data will be modeled on a hexagonal grid. See [json schema](https://json-schema.org/learn/getting-started-step-by-step.html) for the definition. Each cell has the following attributes:

<pre>
  {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "http://example.com/product.schema.json",
    "title": "Cell",
    "description": "A cell in the hexagonal lattice",
    "type": "object",
    "properties": {
      "x": {"type": "float"},
      "y": {"type": "float"},
      "z": {"type": "float"},
      "noise":{
        "type": "object",
        "properties": {
          "time": {
            "type": "array",
            "description": "The array of noise values for the different time steps. Can be truncated to remove old time steps."
            "items": {"type": float}
          },
          "value": {
            "type": "float",
            "description": "The noise value for the current time step."
          }
        }
      },
      "street": {
        "type": "array",
        "description": "A sparse array which contains for directions a map of directions and probabilities to switch to.",
        "items": {
          "type": "array",
          "description": "A map of direction to probability. The direction is the array index. Assume sorted keys. Values are summed probabilities."
          "items": {"type": "float"}
        }
      }
    }
  }
</pre>

## Links

### Straßenverkehrslärm (Study of ADAC, 2006)

[Straßenverkehrslärm](https://www.adac.de/_mmm/pdf/fi_strassenverkehrslaerm_1106_238780.pdf)

### Traffic numbers for Dresden

Open the [Themenstadtplan of city of Dresden](https://stadtplan2.dresden.de) and select _Themen_ -> _Verkehr_

### Noiselevel and calculations

[Soundpressure](https://de.wikipedia.org/wiki/Schalldruckpegel)

[Calculations](https://www.schweizer-fn.de/akustik/schallpegelaenderung/schallpegel.php)

[Tables](http://www.sengpielaudio.com/TabelleDerSchallpegel.htm)

## Personal Check list

- RStudio installed
- VirtualBox installed (optional)
