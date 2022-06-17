import asyncio
from aiohttp import web
from asyncdeta import Deta
from aiohttp_middlewares import cors_middleware


routes = web.RouteTableDef()


@routes.post('/cdn')
async def make_cdn(request: web.Request):
    project_key = request.headers.get('DETA-PROJECT-KEY')
    drive_name = request.headers.get('DRIVE-NAME')
    file_name = request.headers.get('FILE-NAME')
    if not (project_key and drive_name and file_name):
        return web.json_response(
            {
                'error': 'Missing headers',
                'required': ['DETA-PROJECT-KEY', 'DRIVE-NAME', 'FILE-NAME']
            },
            status=400
        )
    deta = Deta(project_key)
    await deta.connect()
    drive = deta.drive(drive_name)
    file = await drive.get(file_name)
    return web.Response(body=file.read(), content_type='image/png')


async def run():
    app = web.Application(middlewares=[cors_middleware(allow_all=True)])
    app.add_routes(routes)
    return app
