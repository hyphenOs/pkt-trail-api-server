"""
A module for generating all the Response messages as per schema.
"""

from pkttrail.schema.messages import (
        OS_AGENT_INIT_MESSAGE,
        OS_AGENT_KEEPALIVE_MESSAGE,
        JSON_RPC_VERSION_2,
        method_to_schema_class
    )

from pkttrail.schema.messages import (
        PktTrailInitResponseSchema,
        PktTrailKeepAliveResponseSchema
    )

def get_api_response_ok(method, msgid):
    """ Return a Simple Success Response."""

    try:
        classes = method_to_schema_class[method]
        schema = classes['response']
    except KeyError:
        return _get_api_response_error_bad_method(msgid)

    response_dict = dict(
        jsonrpc=JSON_RPC_VERSION_2,
        id=msgid,
        result=dict(status="ok"))

    return schema().dump(response_dict)


def _get_api_response_error_bad_method(msgid):
    """ Return Unknown Method Error Response."""
    response_dict = dict(
        jsonrpc=JSON_RPC_VERSION_2,
        error=dict(code=-32601,
            message="Method not found",
            id=msgid))

    return response_dict
