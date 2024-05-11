<!-- markdownlint-disable MD024 MD026 -->

# REST_05 server API Documentation

## Clear LEDs

### URL: `/api/v1/leds`

#### Method: `DELETE`

#### Data Params:

Optional:

- `color` : A JSON string representing an RGB color. Each color value should be between 0 and 255.
- Content example: `{"color": [0, 128, 0]}`

#### Success Response:

- Code: 200
- Content: `{"message": "LEDs cleared"}`

#### Error Response:

- Code: 400
- Content: `{"error": "Invalid JSON"}` OR `{"error": "Invalid color value"}` OR `{"error": "Invalid color type"}`

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
