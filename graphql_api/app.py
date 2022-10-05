import traceback

import falcon.asgi
from falcon.request import Request
from falcon.response import Response

from graphql_api.schema import schema
from . import logger


class GraphqlResource:
    async def on_post(self, req: Request, resp: Response):
        query = await req.media
        try:
            result = await schema.execute_async(
                query['query'],
                variables=query['variables']
            )
        except Exception as exc:
            logger.info(f"Exception {exc} while executing query {query}")
            logger.info(traceback.format_exc())
            resp.status = falcon.HTTP_500
            return
        if result.errors:
            logger.warning(f'Error - {result.errors } - occured while '
                           f'processing query - {query}')
        result_json = {
            "success": False if result.errors else True,
            "data": result.data,
            # returning only the error message
            "errors": str(result.errors[0].original_error)
            if result.errors else None,
        }
        resp.media = result_json


def create_app():
    app = falcon.asgi.App()
    app.add_route('/graphql', GraphqlResource())
    return app
