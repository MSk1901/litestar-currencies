from litestar.config.cors import CORSConfig

from src.config.settings import config

cors_config = CORSConfig(
    allow_origins=config.app.CORS_ORIGIN,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
    expose_headers=["*"],
)
