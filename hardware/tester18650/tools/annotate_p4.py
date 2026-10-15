"""Continue P3 with source-derived pin legends; leave copper and mechanics intact."""
import json
from pathlib import Path
import pcbnew as k

root = Path(__file__).resolve().parents[1]
assert k.GetBuildVersion().startswith('10.')
path = root / 'tester18650.kicad_pcb'
board = k.LoadBoard(str(path))
assert board.GetTitleBlock().GetRevision() == 'P3', 'One-time P3 -> P4 annotation update'
source = json.loads((root / 'pcb_sources/reference-geometry.json').read_text())
fps = {fp.GetReference(): fp for fp in board.GetFootprints()}
lib = root / 'footprints/Tester18650.pretty'
v = lambda x, y: k.VECTOR2I(k.FromMM(x), k.FromMM(y))
before = sorted((str(t.GetNetname()), t.GetStart().x, t.GetStart().y,
                 t.GetEnd().x, t.GetEnd().y, t.GetWidth(), t.GetLayer())
                for t in board.GetTracks())


def annotation(ref, text, x, y, size=.7):
    """Keep the library and placed footprint legends identical, on F.Fab only."""
    fp = fps[ref]
    item = k.PCB_TEXT(fp)
    item.SetText(text)
    item.SetLayer(k.F_Fab)
    item.SetPosition(fp.GetPosition() + v(x, y))
    item.SetTextSize(v(size, size))
    item.SetTextThickness(k.FromMM(.12))
    fp.Add(item)
    library = lib / (str(fp.GetFPID().GetLibItemName()) + '.kicad_mod')
    content = library.read_text().rstrip()
    assert content.endswith(')')
    entry = (f'(fp_text user {json.dumps(text)} (at {x} {y}) (layer "F.Fab") '
             f'(effects (font (size {size} {size}) (thickness .12))))')
    library.write_text(content[:-1] + '\n' + entry + '\n)\n')


# Names are copied from the cited manufacturer's library, not another tester's
# wiring diagram. RSV@0..5 remain source names; no clone-specific SD mapping.
names = {'D5': 'D5/G14', 'D4': 'D4/G2', 'D1': 'D1/G5',
         '5V': '5V REF'}
for pad in source['nodemcu']['pads']:
    name = pad['name']
    caption = names.get(name, name if name.startswith('RSV@') else name.split('@')[0])
    x, y = -float(pad['x']), float(pad['y'])
    annotation('J1', caption, 9.8 if x > 0 else -9.8, y)
annotation('J1', 'PIN NAMES: SOURCE CAD', 0, -6.7, .65)
annotation('J1', 'CLONE FIT UNVERIFIED', 0, -4.7, .65)
annotation('J2', 'IN- / PAD 6', 12, -5.7)
annotation('J2', 'IN+ / PAD 5', 12, 5.7)
annotation('Q1', 'B/C/E NETS UNASSIGNED', 0, 8, .65)
annotation('K1', '6V COIL / 5V DRIVE', 0, -7.5, .65)
annotation('K1', 'A1:+5V  A2:K1_C', 0, -5.5, .65)

# A dense title at the top used to overlap the newly identified header pins.
fp = fps['J1']
for item in fp.GraphicalItems():
    if hasattr(item, 'GetText') and item.GetText() == 'NODEMCU CH340 REF':
        item.SetText('CH340 REF')
        item.SetPosition(fp.GetPosition() + v(0, -10))
        item.SetTextSize(v(.8, .8))
p = lib / (str(fp.GetFPID().GetLibItemName()) + '.kicad_mod')
s = p.read_text()
s = s.replace('(fp_text user "NODEMCU CH340 REF" (at 0 -18.5)',
              '(fp_text user "CH340 REF" (at 0 -10)')
# The library's .8 vs placed .8 size must match, without altering other texts.
s = s.replace('(fp_text user "CH340 REF" (at 0 -10) (layer "F.SilkS") '
              '(effects (font (size 1 1)',
              '(fp_text user "CH340 REF" (at 0 -10) (layer "F.SilkS") '
              '(effects (font (size .8 .8)')
p.write_text(s)
for drawing in board.GetDrawings():
    if isinstance(drawing, k.PCB_TEXT) and drawing.GetText() == 'P3 / 116x132 / NOT FOR FAB':
        drawing.SetText('P4 / 116x132 / NOT FOR FAB')
board.GetTitleBlock().SetRevision('P4')
board.GetTitleBlock().SetTitle('Tester 18650 / P4 - pin legends - NOT FOR FAB')
board.GetTitleBlock().SetComment(0, 'F.Fab legends from source CAD; module fit and physical wiring unverified.')
board.GetTitleBlock().SetComment(1, 'B.Cu PDF uses TOP registration, matching the already mirrored underside photo.')
after = sorted((str(t.GetNetname()), t.GetStart().x, t.GetStart().y,
                t.GetEnd().x, t.GetEnd().y, t.GetWidth(), t.GetLayer())
               for t in board.GetTracks())
assert before == after, 'Annotation update must not change electrical routing'
k.SaveBoard(str(path), board)
p = root / 'reports/pcb/placement-map.json'
data = json.loads(p.read_text())
data['revision'] = 'P4'
data['note'] += ' P4 adds source CAD pin legends only; all P3 tracks, pads, models and placements retained.'
p.write_text(json.dumps(data, indent=2) + '\n')
print('P4 saved: 30 source-derived NodeMCU pin legends, INA IN+/IN- and explicit Q1 status. All 33 tracks unchanged.')
