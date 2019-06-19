# ground-station-web-client
run on the server, access as a webpage from anywhere! 

### How to use:

Install dependencies:

`pip install -r requirements.txt`

(in a seperate terminal) Start up the launch emulator, which fills
`datastream` fifo file with random numbers as fake data

`python fifo_filler.py`

Leave `fifo_filler` running in a sperate terminal so the client has a fresh stream of data to read
in real time.

Start the server, and go to its local url in a browser.

`python server.py`


Put the tiles in `./data/`:

<https://openmaptiles.com/downloads/tileset/osm/north-america/us/new-mexico/>



You'll also need to download and run the docker tiles server:

```
curl -sSL https://get.docker.com/ | sh
docker run --rm -it -v $(pwd):/data -p 8080:80 klokantech/openmaptiles-server
```

Oh and don't forget some javascript files in js:

https://raw.githubusercontent.com/mapbox/mapbox-gl-leaflet/master/leaflet-mapbox-gl.js
