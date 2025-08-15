from litestar.openapi import OpenAPIConfig

openapi_config = OpenAPIConfig(
    title="OpenAPI для курсов валют",
    version="1.0",
    path="/api/docs",
    use_handler_docstrings=True,
)
