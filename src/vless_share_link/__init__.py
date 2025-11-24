_SPIDER_LEN = 8


def build(outbound_obj: dict, desc: str = ''):
    """Build a share URL from the outbound object and description.

    Reference: https://github.com/XTLS/Xray-core/discussions/716
    """
    import secrets
    from urllib.parse import quote

    i = outbound_obj
    params = {}

    # Base URL components
    protocol = i['protocol']
    uuid = quote(i['settings']['vnext'][0]['users'][0]['id'])
    remote_host = quote(i['settings']['vnext'][0]['address'])
    remote_port = i['settings']['vnext'][0]['port']

    descriptive_text = quote(desc)
    params['type'] = i['streamSettings']['network']

    params['security'] = i['streamSettings'].get('security', 'none')

    match params['type']:
        case 'xhttp':
            params['path'] = quote(
                i['streamSettings']['xhttpSettings'].get('path', '/')
            )
        case _:
            raise NotImplementedError(f'Unsupported type: {params["type"]}')

    match params['security']:
        case 'reality':
            params['fp'] = i['streamSettings']['realitySettings']['fingerprint']
            params['sni'] = quote(i['streamSettings']['realitySettings']['serverName'])
            params['pbk'] = quote(i['streamSettings']['realitySettings']['publicKey'])
            params['spx'] = quote('/' + secrets.token_urlsafe(_SPIDER_LEN))
        case _:
            raise NotImplementedError(f'Unsupported security: {params["security"]}')

    base_url = f'{protocol}://{uuid}@{remote_host}:{remote_port}'
    params_str = '&'.join(f'{k}={v}' for k, v in params.items() if v is not None)
    share_url = f'{base_url}?{params_str}#{descriptive_text}'
    return share_url
