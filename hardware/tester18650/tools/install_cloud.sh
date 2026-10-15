#!/bin/sh
# Local KiCad 10 CLI for this Debian 13 amd64 cloud image. No root required.
set -eu
case "$(uname -m)" in x86_64) ;; *) echo 'This installer requires amd64.' >&2; exit 1 ;; esac
python3 - <<'PY'
import hashlib
import subprocess
import urllib.request
from pathlib import Path

base = Path('/workspace/.tools/kicad10')
packages = base / 'downloads'
packages.mkdir(parents=True, exist_ok=True)
prefix = base / '10.0.4'
origin = 'https://ppa.launchpadcontent.net/kicad/kicad-10.0-releases/ubuntu/'
artifacts = [
    ('kicad-questing.deb', 'pool/main/k/kicad/kicad_10.0.4~ubuntu25.10.1_amd64.deb',
     'fe312104b363c409186eecc764131db590a9382dd40f5effc5516a769e3379b0'),
    ('kicad-symbols-questing.deb', 'pool/main/k/kicad-library-symbols/kicad-symbols_10.0.4~ubuntu25.10.1_all.deb',
     'ed3165109290ae340aa6926fd93f6f4c262d2986b7c3ea9d55ae060af24aed6c'),
]
for name, path, expected in artifacts:
    output = packages / name
    if not output.exists():
        urllib.request.urlretrieve(origin + path, output)
    actual = hashlib.sha256(output.read_bytes()).hexdigest()
    if actual != expected:
        raise SystemExit(f'SHA-256 verification failed: {name}; stop, do not use this artifact.')
    subprocess.run(['dpkg-deb', '-x', str(output), str(prefix)], check=True)
    print(f'{name}: SHA-256 verified')
PY
mkdir -p /workspace/.tools/apt/lists/partial /workspace/.tools/apt/cache/archives/partial /workspace/.tools/apt/empty
cat > /workspace/.tools/apt/sources.list <<'EOF'
deb [signed-by=/usr/share/keyrings/debian-archive-keyring.gpg] https://deb.debian.org/debian trixie main
EOF
# Load before system apt.conf.d, avoiding unrelated system hooks and root paths.
cat > /workspace/.tools/apt/apt.conf <<'EOF'
Dir::Etc::main "/dev/null";
Dir::Etc::parts "/workspace/.tools/apt/empty";
Dir::Etc::sourcelist "/workspace/.tools/apt/sources.list";
Dir::Etc::sourceparts "/workspace/.tools/apt/empty";
Dir::State::lists "/workspace/.tools/apt/lists";
Dir::Cache "/workspace/.tools/apt/cache";
APT::Sandbox::User "agent";
Acquire::Languages "none";
EOF
APT_CONFIG=/workspace/.tools/apt/apt.conf apt-get update
APT_CONFIG=/workspace/.tools/apt/apt.conf apt-get --download-only --assume-yes -o Debug::NoLocking=true install libwxgtk-webview3.2-1t64
python3 - <<'PY'
import subprocess
from pathlib import Path
for artifact in Path('/workspace/.tools/apt/cache/archives').glob('*.deb'):
    subprocess.run(['dpkg-deb', '-x', str(artifact), '/workspace/.tools/kicad10/10.0.4'], check=True)
PY
tester_installer_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
"$tester_installer_dir/kicad.sh" version
# Exercise the actual schematic backend without changing tracked artifacts.
tester_smoke_dir=$(mktemp -d /tmp/tester18650-install-check.XXXXXX)
"$tester_installer_dir/kicad.sh" sch export pdf --exclude-pdf-property-popups --output "$tester_smoke_dir/tester18650.pdf" "$tester_installer_dir/../tester18650.kicad_sch"
tester_smoke_exit=0
"$tester_installer_dir/kicad.sh" sch erc --format json --severity-all --exit-code-violations --output "$tester_smoke_dir/erc.json" "$tester_installer_dir/../tester18650.kicad_sch" || tester_smoke_exit=$?
[ "$tester_smoke_exit" -eq 5 ] || { echo "Unexpected ERC smoke status: $tester_smoke_exit" >&2; exit 1; }
printf 'Local KiCad backend verified. PDF and non-clean ERC report: %s\n' "$tester_smoke_dir"
