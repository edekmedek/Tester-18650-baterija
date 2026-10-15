#!/bin/sh
set -eu
tester_pcb_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$tester_pcb_dir"
mkdir -p reports/pcb
./tools/kicad.sh version > reports/pcb/kicad-version.txt
case "$(cat reports/pcb/kicad-version.txt)" in 10.*) ;; *) echo 'KiCad 10 required' >&2; exit 1 ;; esac
./tools/kicad.sh pcb export pdf --layers F.Cu,F.SilkS,F.Fab,Edge.Cuts --mode-single --include-border-title --sketch-pads-on-fab-layers --no-property-popups --black-and-white --scale 1 --output tester18650_pcb_layout.pdf tester18650.kicad_pcb
./tools/kicad.sh pcb export glb --force --include-tracks --include-pads --include-silkscreen --include-soldermask --user-origin 90x25mm --output tester18650_pcb_3d.glb tester18650.kicad_pcb
tester_pcb_drc=0
./tools/kicad.sh pcb drc --schematic-parity --all-track-errors --severity-all --format json --exit-code-violations --output reports/pcb/drc.json tester18650.kicad_pcb || tester_pcb_drc=$?
printf 'Native PCB DRC exit status: %s\n' "$tester_pcb_drc" > reports/pcb/drc-exit-status.txt
if [ "$tester_pcb_drc" -ne 5 ]; then echo "Unexpected DRC status: $tester_pcb_drc (draft still has open connections)" >&2; exit 1; fi
tester_pcb_text_drc=0
./tools/kicad.sh pcb drc --schematic-parity --all-track-errors --severity-all --format report --exit-code-violations --output reports/pcb/drc.rpt tester18650.kicad_pcb || tester_pcb_text_drc=$?
[ "$tester_pcb_text_drc" -eq "$tester_pcb_drc" ] || exit 1
python3 tools/check_pcb.py > reports/pcb/board-check.txt
cat reports/pcb/board-check.txt
blender --version > reports/pcb/blender-version.txt
# Avoid accepting an image left behind by a failed render.
rm -f tester18650_pcb_3d.png
blender -b --python-exit-code 2 --python tools/render_pcb.py > reports/pcb/render.log 2>&1
[ -s tester18650_pcb_3d.png ]
sha256sum tester18650.kicad_pcb tester18650_pcb_layout.pdf tester18650_pcb_3d.glb tester18650_pcb_3d.png reports/pcb/drc.json reports/pcb/drc.rpt reports/pcb/board-check.txt pcb_sources/reference-geometry.json pcb_sources/p2/geometry.json reports/pcb/p2-models.json models/RT314006_DIMENSION_REFERENCE_NO_PINS.step models/Cement_5WAXIAL_VERTICAL_SUBSTITUTE.step models/Keystone1042_REFERENCE_NO_MOUNTING.step > reports/pcb/SHA256SUMS
printf 'PCB outputs verified. Preserving NON-CLEAN native DRC status %s.\n' "$tester_pcb_drc"
exit "$tester_pcb_drc"
