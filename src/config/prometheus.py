from litestar.plugins.prometheus import PrometheusConfig, PrometheusController

prometheus_config = PrometheusConfig(app_name="currencies")
prometheus_controller = PrometheusController
