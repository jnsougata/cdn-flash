import asyncio
from aiohttp import web
from asyncdeta import Deta
from aiohttp_middlewares import cors_middleware


routes = web.RouteTableDef()


@routes.get('/')
async def index(request):
    return web.json_response({'status': 'ok'})


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
    local_name = file.name.split('/')[-1]
    with open(local_name, 'wb') as f:
        f.write(await file.read())
    await deta.close()
    return web.json_response({'url': f'https://cdn-flash.herokuapp.com/file/{file_name}'})


@routes.get('/file/{file_name}')
async def get_file(request: web.Request):
    file_name = request.match_info['file_name']
    if file_name:
        return web.FileResponse(file_name)


async def run():
    """Binds the app to an available port and runs the server."""
    app = web.Application(middlewares=[cors_middleware(allow_all=True)])
    app.add_routes(routes)
    return app

if __name__ == '__main__':
    web.run_app(run())
