from fastapi import FastAPI
from .routes import artists, events, venues, multimedia_endpoints, auth
import uvicorn

from .config import config

app = FastAPI(
    title='Artist Scout API',
    contact={'email': 'el19055@mail.ntua.gr'},
    license={
        'name': 'Apache 2.0',
        'url': 'http://www.apache.org/licenses/LICENSE-2.0.html',
    },
    version='1.0.0',
    servers=[{'url': 'http://127.0.0.1/'}],
)

app.include_router(artists.router)
app.include_router(events.router)
app.include_router(multimedia_endpoints.router)
app.include_router(venues.router)
app.include_router(auth.router)

if __name__ == "__main__":
    uvicorn.run(app=app, host=config.server_address, port=config.port)


