#!/bin/sh
set -eu
# Match the Python API to the native KiCad 10 installation.
tester_api=/workspace/.tools/kicad10/10.0.4
if [ -f "$tester_api/usr/lib/python3/dist-packages/pcbnew.py" ]; then
    export PYTHONPATH="$tester_api/usr/lib/python3/dist-packages${PYTHONPATH:+:$PYTHONPATH}"
    export LD_LIBRARY_PATH="$tester_api/usr/lib/x86_64-linux-gnu${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
fi
export XDG_CONFIG_HOME=/tmp/tester18650-kicad-python/config
export XDG_CACHE_HOME=/tmp/tester18650-kicad-python/cache
export XDG_DATA_HOME=/tmp/tester18650-kicad-python/data
mkdir -p "$XDG_CONFIG_HOME" "$XDG_CACHE_HOME" "$XDG_DATA_HOME"
exec /usr/bin/python3 "$@"
