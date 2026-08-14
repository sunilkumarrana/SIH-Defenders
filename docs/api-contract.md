# API Contract - SIH-Defenders

## POST /detect
- **Request**: `multipart form-data { file: image, lat: float, lon: float }`
- **Response**: `{ "id": int, "pothole_count": int, "severity": "low"|"medium"|"high", "lat": float, "lon": float }`

## GET /reports
- **Response**: `[ { "id": int, "lat": float, "lon": float, "severity": str, "image_url": str, "pothole_count": int, "timestamp": str, "status": "pending"|"fixed" } ]`

## GET /reports/{id}
- **Response**: `single report object (same shape as above)`

## PATCH /reports/{id}
- **Request**: `{ "status": "fixed" }`
- **Response**: `updated report object`
