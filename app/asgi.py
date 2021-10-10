from app.factory import create_app
from app.settings import get_settings

app, settings = create_app(get_settings())
