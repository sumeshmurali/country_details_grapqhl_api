import traceback

import falcon.asgi
from . import logger

from falcon.request import Request
from falcon.response import Response

from graphql_api.schema import schema


class GraphqlResource:
    async def on_post(self, req: Request, resp: Response):
        query = await req.media
        try:
            result = schema.execute(
                query['query'],
                variables=query['variables']
            )
            result_json = {
                "success": False if result.errors else True,
                "data": result.data,
                # returning only the error message
                "errors": str(result.errors[0].original_error)
                if result.errors else None,
            }
            resp.media = result_json
        except Exception as exc:
            # TODO add logging here
            logger.info(str(exc))
            logger.info(traceback.format_exc())


app = falcon.asgi.App()
app.add_route('/graphql', GraphqlResource())

logger.info("Finished adding routes")
