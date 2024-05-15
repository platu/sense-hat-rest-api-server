<!-- markdownlint-disable MD024 MD026 -->

# REST_04 server API Documentation

## Post Message to the led matrix

### URL: `/api/v1/messages/`

#### Method: `POST`

#### Data Params:

Required:

- `msg`: A string representing the message to be displayed.
- Content example: `{"msg": "Hello, World!"}`

Optional:

- `speed`: An integer representing the speed of the scrolling message.
- `fg`: A JSON string representing an RGB color for the foreground. Each color value should be between 0 and 255.
- `bg`: A JSON string representing an RGB color for the background. Each color value should be between 0 and 255.

#### Success Response:

- Code: 200
- Content: {"message": "Message processed"}

#### Error Response:

- Code: 400
- Content: one of the following:
  - `{"error": "Invalid JSON"}`
  - `{"error": "Missing 'msg' key"}`
  - `{"error": "Invalid 'speed' value"}`
  - `{"error": "Invalid 'fg' value"}`
  - `{"error": "Invalid 'bg' value"}`
  - `{"error": "Invalid color for 'fg'"}`
  - `{"error": "Invalid color for 'bg'"}`
  - `{"error": "Invalid message keys"}`

#### API call examples:

```bash
curl -X POST -H "Content-Type: application/json" \
"http://localhost:8080/api/v1/messages/" \
-d '{"msg": "Hello, World!"}'
{"message": "Message processed"}%
```

```bash
curl -X POST -H "Content-Type: application/json" \
"http://localhost:8080/api/v1/messages/" \
-d '{"msg": "Hello, World!", "speed": 0.02}'
{"message": "Message processed"}%
```

```bash
curl -X POST -H "Content-Type: application/json" \
"http://localhost:8080/api/v1/messages/" \
-d '{"msg": "Hello, World!", "speed": 0.05, "fg": [0, 128, 0], "bg": [0, 0, 64]}'
{"message": "Message processed"}%
```

For all other API call examples, refer to the [pytest test_04.py](../test_04.py) file.
