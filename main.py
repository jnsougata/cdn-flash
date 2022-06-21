import os
import asyncio
import secrets
from aiohttp import web
from asyncdeta import Deta
from aiohttp_middlewares import cors_middleware


routes = web.RouteTableDef()
MAX_SIZE = 1024 * 1024 * 50


@routes.get('/')
async def index(request):
    return web.json_response({'status': 'ok'})


@routes.post('/upload')
async def upload(request: web.Request):
    """Uploads a file to the server. will be added soon"""
    return web.json_response({'status': 'ok'})


@routes.get('/url')
async def convert_to_asset(request: web.Request):
    project_key = request.headers.get('DETA-PROJECT-KEY')
    drive_name = request.headers.get('DETA-DRIVE-NAME')
    file_name = request.headers.get('DETA-FILE-NAME')
    if not project_key:
        return web.json_response({'error': 'missing `DETA-PROJECT-KEY` inside headers'}, status=400)
    if not drive_name:
        return web.json_response({'error': 'missing `DETA-DRIVE-NAME` inside headers'}, status=400)
    if not file_name:
        return web.json_response({'error': 'missing `DETA-FILE-NAME` inside headers'}, status=400)

    project_id = project_key.split('_')[0]
    deta = Deta(project_key)
    await deta.connect()
    drive = deta.drive(drive_name)
    file = await drive.get(file_name)
    file_hash = secrets.token_urlsafe(16).lower()
    file_extension = file_name.split('.')[-1]
    path = f"{file_hash}.{file_extension}" if file_extension else f"{file_hash}"
    with open(path, 'wb') as f:
        f.write(file.read(MAX_SIZE))
    await deta.close()

    async def schedule_deletion():
        await asyncio.sleep(3600)
        os.remove(path)
    asyncio.create_task(schedule_deletion())
    return web.json_response({'url': f'https://cdn-flash.herokuapp.com/file/{path}'}, status=200)


@routes.get('/file/{file_name}')
async def deliver_asset(request: web.Request):
    file_name = request.match_info['file_name']
    if file_name and os.path.exists(file_name):
        return web.FileResponse(file_name, status=200)
    return web.json_response({'error': 'file not found'}, status=404)


async def run():
    """Binds the app to an available port and runs the server."""
    print('[----- Running -----]')
    app = web.Application(middlewares=[cors_middleware(allow_all=True)])
    app.add_routes(routes)
    return app

if __name__ == '__main__':
    web.run_app(run())
