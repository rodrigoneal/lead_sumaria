from datetime import datetime
import json
from fastapi import Request
from sumula.api.config.db import get_session
from sumula.api.domain.model import Logs
from sumula.api.domain.repositories.auth_repository import AuthRepository
from starlette.middleware.base import BaseHTTPMiddleware
from sumula.api.domain.repositories.logs_repository import LogsRepository
from sumula.etc.file_handler import async_iterator_wrapper as aiwrap


class CustomHeaderMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        session = await get_session()
        if request.url.query:
            try:
                st_sucesso = False
                auth_repository = AuthRepository(session)
                api_key = request.headers.get("X-API-Key")
                id_usuario = 0
                if user := await auth_repository.check_api_key(api_key):
                    id_usuario = user.id
                chamada = str(request.url)
                start = datetime.now()
                response = await call_next(request)
                if response.status_code == 200:
                    st_sucesso = True
                resp_body = [
                    section async for section in response.__dict__["body_iterator"]
                ]
                response.__setattr__("body_iterator", aiwrap(resp_body))
                response_body = json.loads(resp_body[0].decode())
                logs = Logs(
                    id_client=id_usuario,
                    dh_chamada=start,
                    dh_retorno=datetime.now(),
                    url_chamada=chamada,
                    st_sucesso=st_sucesso,
                    dados_retorno=response_body,
                    cd_ocorrencia=0,
                    ds_erro="",
                )
                logs_repository = LogsRepository(session)
                await logs_repository.save_logs(logs)
                return response
            except Exception as e:
                raise e

        response = await call_next(request)
        return response