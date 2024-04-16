from sanic import Request, response, Blueprint

from qstd_core import openapi
from src.core.config import config

openapi.utils.openapi['info']['title'] = config.project.name
openapi.utils.openapi['info']['version'] = config.project.version
openapi.utils.openapi['x-tagGroups'] = [
    dict(
        name='User',
        tags=['User']
    )
]

raw_html = open(config.root_dir + '/resources/redoc.html', 'r').read()\
    .replace('{DOC_PATH}', config.server.address.docs)


@openapi.exclude()
async def get_docs(_: Request):
    return response.html(raw_html, 200)


docs_router = Blueprint('docs')
docs_router.add_route(get_docs, '/docs', ['GET'])
