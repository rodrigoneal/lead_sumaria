from .sumula_routers import sumula_routers

def add_routers(app):
    app.include_router(sumula_routers)