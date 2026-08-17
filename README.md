# Vision Platform Local

Serviço de captura local para o ecossistema GeoFissura Vision Platform.

## Responsabilidades

- Conectar à câmera IP via RTSP
- Capturar frames em intervalo configurável
- Validar qualidade da imagem (brilho, foco, frame congelado)
- Armazenar evidências com hash SHA-256
- Disponibilizar API local para a Vision Platform Central
- Funcionar offline com fila de entrega

## Stack

- Python 3.11+
- FastAPI + Uvicorn
- OpenCV (opencv-python-headless)
- SQLAlchemy + PostgreSQL
- Pydantic Settings

## Configuração

Copie `.env.example` para `.env` e configure:

```bash
cp .env.example .env
```

## Desenvolvimento

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -e ".[dev]"
ruff check src/ tests/
pytest
```

## Deploy no Orange Pi

```bash
pip install -e .
sudo cp deploy/systemd/vision-platform-local.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable vision-platform-local
sudo systemctl start vision-platform-local
```

## API

| Endpoint | Método | Descrição |
|---|---|---|
| `/health` | GET | Health check com status da câmera e armazenamento |
| `/api/v1/status` | GET | Status do sistema (CPU, memória) |
| `/api/v1/cameras` | GET | Lista de câmeras cadastradas |
| `/api/v1/observations` | GET | Observações com paginação por cursor |
| `/api/v1/observations/{id}/ack` | POST | Confirmação idempotente de recebimento |
