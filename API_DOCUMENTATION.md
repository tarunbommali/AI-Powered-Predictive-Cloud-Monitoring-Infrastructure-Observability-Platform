# API Documentation

Complete API reference for the Cloud Monitoring System.

## Base URL

```
Development: http://localhost:8000/api
Production: https://your-domain.com/api
```

## Authentication

All protected endpoints require JWT Bearer token authentication.

### Get Token

Include the token in the Authorization header:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

## Auth Endpoints

### Register User

Create a new user account.

**Endpoint:** `POST /auth/register`

**Request Body:**
```json
{
  "email": "user@example.com",
  "username": "johndoe",
  "password": "SecurePassword123",
  "full_name": "John Doe"
}
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "johndoe",
  "full_name": "John Doe",
  "is_active": true,
  "is_admin": false,
  "created_at": "2024-01-24T10:30:00Z"
}
```

### Login

Authenticate and get access token.

**Endpoint:** `POST /auth/login`

**Request Body:** (Form Data)
```
username=johndoe
password=SecurePassword123
```

**Response:** `200 OK`
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Get Current User

Get authenticated user information.

**Endpoint:** `GET /auth/me`

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "johndoe",
  "full_name": "John Doe",
  "is_active": true,
  "is_admin": false,
  "created_at": "2024-01-24T10:30:00Z"
}
```

---

## Instance Endpoints

### List Instances

Get all instances for the current user.

**Endpoint:** `GET /instances/`

**Headers:** `Authorization: Bearer <token>`

**Query Parameters:**
- `skip` (int, optional): Number of records to skip (default: 0)
- `limit` (int, optional): Maximum records to return (default: 100)

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "name": "Web Server 1",
    "instance_id": "i-1234567890abcdef0",
    "ip_address": "10.0.1.100",
    "port": 9100,
    "region": "us-east-1",
    "instance_type": "t3.medium",
    "status": "active",
    "is_monitored": true,
    "owner_id": 1,
    "tags": {"environment": "production"},
    "created_at": "2024-01-24T10:00:00Z",
    "updated_at": "2024-01-24T10:00:00Z"
  }
]
```

### Get Instance

Get single instance by ID.

**Endpoint:** `GET /instances/{instance_id}`

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
{
  "id": 1,
  "name": "Web Server 1",
  "instance_id": "i-1234567890abcdef0",
  "ip_address": "10.0.1.100",
  "port": 9100,
  "region": "us-east-1",
  "instance_type": "t3.medium",
  "status": "active",
  "is_monitored": true,
  "owner_id": 1,
  "tags": {},
  "created_at": "2024-01-24T10:00:00Z",
  "updated_at": null
}
```

### Add Instance

Create a new instance.

**Endpoint:** `POST /instances/`

**Headers:** `Authorization: Bearer <token>`

**Request Body:**
```json
{
  "name": "Web Server 1",
  "instance_id": "i-1234567890abcdef0",
  "ip_address": "10.0.1.100",
  "port": 9100,
  "region": "us-east-1",
  "instance_type": "t3.medium",
  "tags": {"environment": "production"}
}
```

**Response:** `201 Created`

### Update Instance

Update an existing instance.

**Endpoint:** `PUT /instances/{instance_id}`

**Headers:** `Authorization: Bearer <token>`

**Request Body:**
```json
{
  "name": "Updated Server Name",
  "is_monitored": false,
  "status": "inactive"
}
```

**Response:** `200 OK`

### Delete Instance

Delete an instance.

**Endpoint:** `DELETE /instances/{instance_id}`

**Headers:** `Authorization: Bearer <token>`

**Response:** `204 No Content`

### Get Instance Alerts

Get alerts for a specific instance.

**Endpoint:** `GET /instances/{instance_id}/alerts`

**Headers:** `Authorization: Bearer <token>`

**Query Parameters:**
- `active_only` (bool, optional): Filter only active alerts (default: true)

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "instance_id": 1,
    "alert_type": "cpu",
    "metric_name": "CPU Usage",
    "threshold_value": 80.0,
    "current_value": 85.5,
    "severity": "warning",
    "message": "CPU usage on Web Server 1 is 85.50%",
    "status": "active",
    "triggered_at": "2024-01-24T11:00:00Z",
    "resolved_at": null
  }
]
```

---

## Metrics Endpoints

### Get CPU Metrics

Get CPU metrics for an instance.

**Endpoint:** `GET /metrics/cpu/{instance_id}`

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
{
  "instance_id": "i-1234567890abcdef0",
  "instance_name": "Web Server 1",
  "timestamp": 1706097600.0,
  "usage_percent": 45.2,
  "per_core": [42.1, 48.3, 44.7, 45.9],
  "load_1min": 2.15,
  "load_5min": 1.98,
  "load_15min": 1.76
}
```

### Get Memory Metrics

Get memory metrics for an instance.

**Endpoint:** `GET /metrics/memory/{instance_id}`

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
{
  "instance_id": "i-1234567890abcdef0",
  "instance_name": "Web Server 1",
  "timestamp": 1706097600.0,
  "total": 16777216000,
  "used": 10485760000,
  "available": 6291456000,
  "usage_percent": 62.5,
  "swap_total": 8388608000,
  "swap_used": 1048576000
}
```

### Get Disk Metrics

Get disk metrics for an instance.

**Endpoint:** `GET /metrics/disk/{instance_id}`

**Headers:** `Authorization: Bearer <token>`

**Query Parameters:**
- `mount_point` (string, optional): Disk mount point (default: "/")

**Response:** `200 OK`
```json
{
  "instance_id": "i-1234567890abcdef0",
  "instance_name": "Web Server 1",
  "timestamp": 1706097600.0,
  "total": 107374182400,
  "used": 32212254720,
  "available": 75161927680,
  "usage_percent": 30.0,
  "read_bytes": 1048576,
  "write_bytes": 2097152
}
```

### Get Network Metrics

Get network metrics for an instance.

**Endpoint:** `GET /metrics/network/{instance_id}`

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
{
  "instance_id": "i-1234567890abcdef0",
  "instance_name": "Web Server 1",
  "timestamp": 1706097600.0,
  "rx_bytes": 15728640,
  "tx_bytes": 10485760,
  "rx_packets": 12500,
  "tx_packets": 8500,
  "rx_errors": 0,
  "tx_errors": 0
}
```

### Get Load Metrics

Get system load and uptime.

**Endpoint:** `GET /metrics/load/{instance_id}`

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
{
  "instance_id": "i-1234567890abcdef0",
  "instance_name": "Web Server 1",
  "timestamp": 1706097600.0,
  "uptime_seconds": 864000,
  "load_1min": 2.15,
  "load_5min": 1.98,
  "load_15min": 1.76
}
```

### Get All Metrics

Get all metrics for an instance in one request.

**Endpoint:** `GET /metrics/all/{instance_id}`

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
{
  "instance_id": "i-1234567890abcdef0",
  "instance_name": "Web Server 1",
  "timestamp": 1706097600.0,
  "cpu": {
    "usage_percent": 45.2,
    "per_core": [42.1, 48.3, 44.7, 45.9],
    "load_1min": 2.15,
    "load_5min": 1.98,
    "load_15min": 1.76
  },
  "memory": {
    "total": 16777216000,
    "used": 10485760000,
    "available": 6291456000,
    "usage_percent": 62.5,
    "swap_total": 8388608000,
    "swap_used": 1048576000
  },
  "disk": {
    "total": 107374182400,
    "used": 32212254720,
    "available": 75161927680,
    "usage_percent": 30.0,
    "read_bytes": 1048576,
    "write_bytes": 2097152
  },
  "network": {
    "rx_bytes": 15728640,
    "tx_bytes": 10485760,
    "rx_packets": 12500,
    "tx_packets": 8500,
    "rx_errors": 0,
    "tx_errors": 0
  },
  "uptime_seconds": 864000
}
```

### Get Dashboard Summary

Get aggregated metrics across all instances.

**Endpoint:** `GET /metrics/dashboard/summary`

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
{
  "total_instances": 5,
  "active_instances": 4,
  "total_alerts": 3,
  "critical_alerts": 1,
  "average_cpu": 45.6,
  "average_memory": 68.2,
  "average_disk": 42.1
}
```

---

## Health Endpoints

### Basic Health Check

Check if API is running.

**Endpoint:** `GET /health/`

**Response:** `200 OK`
```json
{
  "status": "healthy",
  "timestamp": "2024-01-24T12:00:00Z",
  "version": "1.0.0",
  "app": "Cloud Monitoring System"
}
```

### Services Health Check

Check health of all dependent services.

**Endpoint:** `GET /health/services`

**Response:** `200 OK`
```json
{
  "status": "healthy",
  "timestamp": "2024-01-24T12:00:00Z",
  "services": {
    "api": "healthy",
    "prometheus": "healthy"
  }
}
```

---

## Error Responses

### Standard Error Format

```json
{
  "detail": "Error message describing what went wrong"
}
```

### HTTP Status Codes

- `200 OK`: Successful request
- `201 Created`: Resource created successfully
- `204 No Content`: Successful deletion
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Missing or invalid authentication
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `422 Unprocessable Entity`: Validation error
- `500 Internal Server Error`: Server error

### Example Error Responses

**401 Unauthorized:**
```json
{
  "detail": "Could not validate credentials"
}
```

**404 Not Found:**
```json
{
  "detail": "Instance not found"
}
```

**422 Validation Error:**
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "value is not a valid email address",
      "type": "value_error.email"
    }
  ]
}
```

---

## Rate Limiting

API endpoints are rate-limited to prevent abuse:

- **Authentication endpoints**: 5 requests per minute
- **Read endpoints**: 100 requests per minute
- **Write endpoints**: 30 requests per minute

Exceeded rate limits return `429 Too Many Requests`.

---

## Interactive Documentation

- **Swagger UI**: `http://localhost:8000/api/docs`
- **ReDoc**: `http://localhost:8000/api/redoc`
- **OpenAPI JSON**: `http://localhost:8000/api/openapi.json`
