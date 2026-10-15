#!/bin/sh
set -eu
tester_project_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$tester_project_dir"
case "$(./tools/kicad.sh version)" in
    10.*) ;;
    *) echo 'KiCad 10 required.' >&2; exit 1 ;;
esac
mkdir -p reports
./tools/kicad.sh sch export pdf --exclude-pdf-property-popups --output tester18650.pdf tester18650.kicad_sch
./tools/kicad.sh sch export netlist --format kicadxml --output reports/netlist.xml tester18650.kicad_sch
tester_erc_exit=0
./tools/kicad.sh sch erc --format json --severity-all --exit-code-violations --output reports/erc.json tester18650.kicad_sch || tester_erc_exit=$?
printf 'Native ERC exit status: %s\n' "$tester_erc_exit" > reports/erc-exit-status.txt
if [ "$tester_erc_exit" -ne 5 ]; then
    echo "Unexpected ERC exit status: $tester_erc_exit (expected 5 for documented open connections)." >&2
    exit 1
fi
./tools/kicad.sh sch erc --format report --severity-all --exit-code-violations --output reports/erc.rpt tester18650.kicad_sch || tester_report_exit=$?
if [ "${tester_report_exit:-0}" -ne 5 ]; then
    echo "Unexpected text ERC status: ${tester_report_exit:-0}." >&2
    exit 1
fi
python3 tools/check_connectivity.py > reports/connectivity-check.txt
cat reports/connectivity-check.txt
sha256sum tester18650.kicad_pro tester18650.kicad_sch tester18650.pdf reports/erc.json reports/erc.rpt reports/netlist.xml ../../firmware/battery-tester-8266-wifi-test.yaml > reports/SHA256SUMS
printf "ERC is non-clean; preserving native exit status %s.\n" "$tester_erc_exit"
exit "$tester_erc_exit"
