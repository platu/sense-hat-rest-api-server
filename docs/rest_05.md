<!-- markdownlint-disable MD024 MD026 -->

# REST_05 server API Documentation

## Clear LEDs

### URL: `/api/v1/leds`

#### Method: `DELETE`

#### Data Params:

Optional:

- `color`: A JSON string representing an RGB color. Each color value should be between 0 and 255.
- Content example: `{"color": [0, 128, 0]}`

#### Success Response:

- Code: 200
- Content: `{"message": "LEDs cleared"}`

#### Error Response:

- Code: 400
- Content:
  - `{"error": "Invalid JSON"}`
  - `{"error": "Invalid color"}`
  - `{"error": "Invalid color value"}`

#### API call examples:

```bash
curl -X DELETE -H "Content-Type: application/json" \
"http://localhost:8080/api/v1/leds"
{"message": "LEDs cleared"}%
```

```bash
curl -X DELETE -H "Content-Type: application/json" \
"http://localhost:8080/api/v1/leds" \
-d '{"color": "[0, 0, 64]"}'
{"message": "LEDs cleared"}%
```

## Get LEDs

### URL: `/api/v1/leds`

#### Method: `GET`

#### Success Response:

- Code: 200
- Content: a JSON dicti`nary with the 'leds' key containing a list of 64 RGB colors.

#### API call example:

```bash
curl -X GET -H "Content-Type: application/json" \
"http://localhost:8080/api/v1/leds"
{"leds": [[40, 60, 96], [40, 68, 112], [48, 72, 104], [56, 92, 56], [56, 92, 56], [48, 72, 112], [40, 64, 112], [40, 60, 96], [64, 100, 56], [72, 124, 80], [72, 124, 80], [112, 184, 112], [112, 180, 112], [72, 124, 80], [72, 120, 72], [56, 100, 56], [40, 64, 112], [64, 104, 88], [88, 148, 88], [80, 132, 80], [72, 132, 80], [88, 152, 88], [64, 100, 88], [40, 64, 112], [56, 92, 168], [56, 68, 88], [160, 184, 128], [184, 216, 152], [184, 216, 152], [160, 184, 128], [56, 64, 88], [56, 92, 168], [64, 76, 88], [112, 96, 72], [160, 144, 112], [184, 164, 128], [184, 168, 128], [160, 144, 112], [112, 92, 64], [64, 76, 88], [64, 84, 64], [96, 100, 72], [80, 56, 40], [112, 84, 64], [112, 84, 64], [72, 56, 40], [96, 100, 72], [56, 80, 64], [56, 84, 152], [24, 44, 80], [80, 60, 40], [120, 92, 72], [120, 96, 72], [80, 60, 40], [24, 44, 80], [56, 88, 152], [64, 100, 176], [56, 88, 152], [48, 40, 40], [48, 40, 32], [48, 40, 32], [48, 44, 48], [56, 88, 152], [64, 100, 176]]}%
```

## Set LEDs

### URL: `/api/v1/leds`

#### Method: `POST`

#### Data Params:

Required:

- `leds` : list of 64 RGB colors.
- Content example: [yoda.json](../yoda.json)

#### Success Response:

- Code: 200
- Content: `{"message": "LEDs updated"}`

#### Error Response:

- Code: 400
- Content:
  - `{"error": "Invalid JSON"}`
  - `{"error": "Missing 'leds' key"}`
  - `{"error": "Invalid color value"}`
  - `{"error": "Invalid color matrix size"}`

#### API call example:

In the following example, the file `yoda.json` preexists in the current directory. Its content is filled by the `pixelart.py` script which is provided in the `pixelart` folder.

```bash
curl -X POST -H "Content-Type: application/json" \
"http://localhost:8080/api/v1/leds" \
-d @yoda.json
{"message": "LEDs updated"}%
```
