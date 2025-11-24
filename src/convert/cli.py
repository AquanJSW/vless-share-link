import argparse
import json
import secrets
import sys

import yaml

from vless_share_link import build

SPIDER_LEN = 8

parser = argparse.ArgumentParser(
    description="Convert XRay configuration to share link."
)
parser.add_argument(
    "-c",
    '--config',
    required=True,
    help="Path to the XRay configuration file. Use '-' for stdin. "
    "yaml and json are supported.",
)
parser.add_argument("-d", '--description', default='')
parser.add_argument(
    '-t',
    '--to',
    default='l',
    choices=('l', 'y', 'j'),
    help='Output format: l (link), y (yaml), j (json)',
)


def main():
    args = parser.parse_args()
    if args.config == '-':
        conf_str = sys.stdin.read()
    else:
        with open(args.config, 'r', encoding='utf-8') as f:
            conf_str = f.read()

    ext = args.config.split('.')[-1].lower()
    match ext:
        case 'yaml' | 'yml':
            conf = yaml.safe_load(conf_str)
        case 'json':
            conf = json.loads(conf_str)
        case _:
            raise NotImplementedError(f'Unsupported config format: {ext}')

    try:
        conf['outbounds'][0]['streamSettings']['realitySettings']['spiderX'] = (
            '/' + secrets.token_urlsafe(SPIDER_LEN)
        )
    except KeyError:
        pass

    match args.to:
        case 'l':
            ostr = build(conf['outbounds'][0], desc=args.description)
        case 'y':
            ostr = yaml.safe_dump(conf, sort_keys=False)
        case 'j':
            ostr = json.dumps(conf, indent=2)
    print(ostr)


if __name__ == "__main__":
    main()
