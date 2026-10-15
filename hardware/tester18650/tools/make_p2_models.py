"""P2 reference bodies. No unverified C3209 or small-resistor body is generated."""
import json
import math
from pathlib import Path
from OCP.STEPControl import STEPControl_Reader, STEPControl_AsIs
from OCP.STEPCAFControl import STEPCAFControl_Writer
from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCylinder
from OCP.BRepAlgoAPI import BRepAlgoAPI_Common
from OCP.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCP.BRepBndLib import BRepBndLib
from OCP.Bnd import Bnd_Box
from OCP.gp import gp_Pnt, gp_Trsf, gp_Vec, gp_Ax1, gp_Dir, gp_Ax2
from OCP.TDocStd import TDocStd_Document
from OCP.TCollection import TCollection_ExtendedString
from OCP.XCAFDoc import XCAFDoc_DocumentTool, XCAFDoc_ColorType
from OCP.Quantity import Quantity_Color, Quantity_TOC_RGB
from OCP.IFSelect import IFSelect_RetDone

root=Path(__file__).resolve().parents[1]
sources=root/'pcb_sources/p2'
report={}

def bounds(shape):
    b=Bnd_Box();BRepBndLib.Add_s(shape,b)
    return [round(v,5) for v in b.Get()]

def save(name,parts):
    doc=TDocStd_Document(TCollection_ExtendedString('XmlXCAF'))
    shapes=XCAFDoc_DocumentTool.ShapeTool_s(doc.Main())
    colors=XCAFDoc_DocumentTool.ColorTool_s(doc.Main())
    for shape,rgb in parts:
        label=shapes.AddShape(shape,False)
        colors.SetColor(label,Quantity_Color(*rgb,Quantity_TOC_RGB),XCAFDoc_ColorType.XCAFDoc_ColorGen)
    writer=STEPCAFControl_Writer();writer.SetColorMode(True)
    assert writer.Transfer(doc,STEPControl_AsIs)
    assert writer.Write(str(root/'models'/name))==IFSelect_RetDone
    report[name]={'parts_bbox_mm':[bounds(s) for s,_ in parts]}

def read(name):
    r=STEPControl_Reader();assert r.ReadFile(str(sources/name))==IFSelect_RetDone
    r.TransferRoots();return r.OneShape()

def above_board(shape):
    clip=BRepPrimAPI_MakeBox(gp_Pnt(-100,-100,0),200,200,100).Shape()
    result=BRepAlgoAPI_Common(shape,clip);result.Build()
    assert result.IsDone()
    return result.Shape()

relay=above_board(read('relay-library.step'))
assert all(abs(a-b)<.002 for a,b in zip(bounds(relay),[-2.35,-2.6,0,26.65,10.1,15.7]))
shift=gp_Trsf();shift.SetTranslation(gp_Vec(-12.15,-3.75,0))
relay=BRepBuilderAPI_Transform(relay,shift,True).Shape()
turn=gp_Trsf();turn.SetRotation(gp_Ax1(gp_Pnt(0,0,0),gp_Dir(0,0,1)),math.pi/2)
relay=BRepBuilderAPI_Transform(relay,turn,True).Shape()
save('RT314006_DIMENSION_REFERENCE_NO_PINS.step',[(relay,(.88,.27,.055))])
report['RT314006_DIMENSION_REFERENCE_NO_PINS.step']['status']='Dimension-matched KiCad body reference, NOT TE STEP. All pin geometry removed; no terminal mapping claimed.'

holder=above_board(read('keystone-1042-library.step'))
holder=BRepBuilderAPI_Transform(holder,turn,True).Shape()
save('Keystone1042_REFERENCE_NO_MOUNTING.step',[(holder,(.10,.105,.12))])
report['Keystone1042_REFERENCE_NO_MOUNTING.step']['status']='Keystone 1042 reference, NOT identified photographed holder. Underboard posts cropped; no manufacturing pads or holes.'

# A concrete library-documented 5W AXIAL substitute, standing on end at the
# crop's 7.62 mm pitch. Standoff/lead forming are NEW design choices, not a
# claimed measurement of the photographed resistor. No 0.25W body is substituted.
body=BRepPrimAPI_MakeBox(gp_Pnt(-3.2,-7.01,1),6.4,6.4,25).Shape()
def wire(a,b):
    vector=gp_Vec(gp_Pnt(*a),gp_Pnt(*b))
    return BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(*a),gp_Dir(vector)),.4,vector.Magnitude()).Shape()
parts=[(body,(.88,.86,.79))]
for a,b in [((0,-3.81,-3),(0,-3.81,1)),((0,-3.81,26),(0,-3.81,27.2)),
            ((0,-3.81,27.2),(0,3.81,27.2)),((0,3.81,27.2),(0,3.81,-3))]:
    parts.append((wire(a,b),(.55,.57,.6)))
save('Cement_5WAXIAL_VERTICAL_SUBSTITUTE.step',parts)
report['Cement_5WAXIAL_VERTICAL_SUBSTITUTE.step']['status']='Proposed 5W AXIAL 22 substitute, body 25x6.4x6.4 from KiCad generator/source model. 1 mm standoff, 0.8 mm graphic wire and forming are design references, NOT validated original dimensions or lead-forming instruction.'
(root/'reports/pcb/p2-models.json').write_text(json.dumps(report,indent=2)+'\n')
print('P2 relay/holder reference bodies and two-instance resistor substitute model created.')
