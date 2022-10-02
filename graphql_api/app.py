import json

import falcon
import falcon.asgi

from falcon.request import Request
from falcon.response import Response

from graphql_api.schema import schema


class GraphqlResource:

    async def on_get(self, req: Request, resp: Response):
        """Handles GET requests"""
        quote = {
            'quote': (
                "I've always been more interested in "
                "the future than in the past."
            ),
            'author': 'Grace Hopper'
        }

        resp.text = json.dumps(quote)

    async def on_post(self, req: Request, resp: Response):
        query = await req.media
        print(query)


app = falcon.asgi.App()
app.add_route('/graphql', GraphqlResource())
