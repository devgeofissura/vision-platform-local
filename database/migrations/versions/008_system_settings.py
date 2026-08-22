"""create system_settings table with seed defaults

Revision ID: 008_system_settings
Revises: 007_proc_status
Create Date: 2026-08-22

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "008_sys_settings"
down_revision: Union[str, None] = "007_proc_status"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

SEED_SETTINGS = [
    # Geral
    ("local_id", "sl000001", "Identificador único deste local"),
    ("local_name", "Orange Pi 001", "Nome amigável do local"),
    ("timezone", "America/Sao_Paulo", "Fuso horário"),

    # Captura global
    ("capture_interval_minutes", "60", "Intervalo padrão de captura em minutos"),
    ("capture_evidence_dir", "/var/lib/vision-platform-local/evidence", "Diretório de evidências"),
    ("capture_jpeg_quality", "90", "Qualidade JPEG padrão (1-100)"),
    ("capture_width", "1920", "Largura padrão da captura"),
    ("capture_height", "1080", "Altura padrão da captura"),

    # Câmera padrão
    ("camera_default_username", "admin", "Usuário padrão das câmeras"),
    ("camera_default_password", "", "Senha padrão das câmeras"),
    ("camera_default_stream_type", "main", "Stream padrão (main ou sub)"),
    ("camera_default_channel", "1", "Canal padrão"),
    ("camera_default_transport", "tcp", "Transporte RTSP padrão"),
    ("camera_connect_timeout_ms", "10000", "Timeout de conexão RTSP (ms)"),

    # Entrega (central)
    ("delivery_interval_seconds", "60", "Intervalo de entrega à central (s)"),
    ("central_api_base_url", "", "URL da API central"),
    ("central_api_token", "", "Token de autenticação da central"),

    # MQTT
    ("mqtt_broker_host", "localhost", "Host do broker MQTT"),
    ("mqtt_broker_port", "1883", "Porta do broker MQTT"),
    ("mqtt_username", "", "Usuário MQTT"),
    ("mqtt_password", "", "Senha MQTT"),
    ("mqtt_topic_prefix", "geofissura/", "Prefixo dos tópicos MQTT"),
    ("mqtt_enabled", "false", "Habilitar cliente MQTT"),

    # Processamento
    ("processing_enabled", "false", "Habilitar processamento de visão"),
    ("processing_auto_on_capture", "true", "Processar automaticamente ao capturar"),
]


def upgrade() -> None:
    op.create_table(
        "system_settings",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("key", sa.String(128), nullable=False, unique=True),
        sa.Column("value", sa.Text(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_system_settings_key", "system_settings", ["key"], unique=True)

    settings_table = sa.table(
        "system_settings",
        sa.column("key", sa.String(128)),
        sa.column("value", sa.Text()),
        sa.column("description", sa.Text()),
    )
    op.bulk_insert(settings_table, [
        {"key": k, "value": v, "description": d} for k, v, d in SEED_SETTINGS
    ])


def downgrade() -> None:
    op.drop_index("ix_system_settings_key", table_name="system_settings")
    op.drop_table("system_settings")
