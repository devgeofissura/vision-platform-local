from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}

    local_id: str = "LOCAL-001"
    local_name: str = "Central Orange Pi 001"
    timezone: str = "America/Sao_Paulo"

    camera_id: str = "GeoFissura_CAM_000001"
    camera_name: str = "VIPC-1230-B-G2 geofissura"
    camera_hostname: str = "geofissuracam01"
    camera_username: str = "admin"
    camera_password: str = ""
    camera_auto_discover: bool = True
    camera_stream_type: str = "main"
    camera_channel: int = 1
    camera_rtsp_url: str = "rtsp://admin:@geofissuracam01:554/cam/realmonitor?channel=1&subtype=0"
    camera_rtsp_transport: str = "tcp"
    camera_connect_timeout_ms: int = 10000
    camera_reconnect_interval_ms: int = 5000
    camera_capture_interval_ms: int = 60000
    camera_capture_width: int = 1920
    camera_capture_height: int = 1080
    camera_capture_jpeg_quality: int = 90

    local_data_dir: str = "/var/lib/vision-platform-local"
    local_evidence_dir: str = "/var/lib/vision-platform-local/evidence"
    local_db_url: str = "postgresql://vision:change-me@localhost:5432/vision_local"
    local_api_host: str = "0.0.0.0"
    local_api_port: int = 8080
    local_api_token: str = "change-me"

    central_api_base_url: str = "http://192.168.1.20:8081"
    central_api_token: str = "change-me"
    central_delivery_interval_ms: int = 60000


settings = Settings()
