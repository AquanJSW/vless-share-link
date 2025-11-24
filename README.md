# VLess/VMess Share Link Generator

Only support xhttp-reality for now.

## Usage

```
usage: convert [-h] -c CONFIG [-d DESCRIPTION] [-t {l,y,j}]

Convert XRay configuration to share link.

options:
  -h, --help            show this help message and exit
  -c, --config CONFIG   Path to the XRay configuration file. Use '-' for stdin. yaml and json are supported.
  -d, --description DESCRIPTION
  -t, --to {l,y,j}      Output format: l (link), y (yaml), j (json)
```

Reference: https://github.com/XTLS/Xray-core/discussions/716