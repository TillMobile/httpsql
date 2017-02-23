import falcon
import settings


class BasicAuthMiddleware(object):
    def process_request(self, req, resp):
        if settings.BASIC_AUTH_USER and settings.BASIC_AUTH_PASSWORD:
            authorization = req.get_header("Authorization")
            if not authorization:
                raise falcon.HTTPError(falcon.HTTP_401, "Unauthorized", "")
        
            chunks = authorization.split(" ")
            try:
                auth_chunks = chunks[1].strip().decode("base64").split(":")
            except Exception, e:
                raise falcon.HTTPError(falcon.HTTP_401, "Unauthorized", "")

            if auth_chunks[0] != settings.BASIC_AUTH_USER or auth_chunks[1] != settings.BASIC_AUTH_PASSWORD:
                raise falcon.HTTPError(falcon.HTTP_401, "Unauthorized", "")
