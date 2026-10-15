#!/bin/sh
set -eu
# Use a native KiCad 10 installation, or the verified local cloud installation.
if [ -n "${KICAD_CLI:-}" ]; then
    tester_kicad_cli=$KICAD_CLI
elif [ -x /workspace/.tools/kicad10/10.0.4/usr/bin/kicad-cli ]; then
    tester_kicad_cli=/workspace/.tools/kicad10/10.0.4/usr/bin/kicad-cli
else
    tester_kicad_cli=$(command -v kicad-cli)
fi
case "$tester_kicad_cli" in
    /workspace/.tools/kicad10/10.0.4/*)
        export LD_LIBRARY_PATH=/workspace/.tools/kicad10/10.0.4/usr/lib/x86_64-linux-gnu${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}
        export KICAD10_SYMBOL_DIR=/workspace/.tools/kicad10/10.0.4/usr/share/kicad/symbols
        ;;
esac
tester_kicad_state="${TMPDIR:-/tmp}/tester18650-kicad-$(id -u)"
export XDG_CONFIG_HOME="$tester_kicad_state/config"
export XDG_CACHE_HOME="$tester_kicad_state/cache"
export XDG_DATA_HOME="$tester_kicad_state/data"
mkdir -p "$XDG_CONFIG_HOME" "$XDG_CACHE_HOME" "$XDG_DATA_HOME"
exec "$tester_kicad_cli" "$@"
