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
- Content: `{"error": "Invalid JSON"}` OR `{"error": "Invalid color value"}` OR `{"error": "Invalid color type"}`

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

## Set LEDs

### URL: `/api/v1/leds`

#### Method: `POST`

#### Data Params:

Required:

- `leds` : A JSON string representing a matrix of LEDs.
- Content example: [yoda.json](../yoda.json)

#### Success Response:

- Code: 200
- Content: `{"message": "LEDs processed"}`

#### Error Response:

- Code: 400
- Content: `{"error": "Invalid JSON"}` OR `{"error": "Missing 'leds' key"}` OR `{"error": "Invalid matrix size"}`

#### API call example:

In the following example, the file `yoda.json` preexists in the current directory. Its content is filled by the `pixelart.py` script which is provided in the `pixelart` folder.

```bash
curl -X POST -H "Content-Type: application/json" \
"http://localhost:8080/api/v1/leds" \
-d @yoda.json
{"message": "LEDs processed"}%
```
