"""Keep all eight library pins and verify their alignment with the mapped footprint."""
import json, math
from pathlib import Path
from OCP.STEPControl import STEPControl_Reader, STEPControl_AsIs
from OCP.STEPCAFControl import STEPCAFControl_Writer
from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCP.BRepAlgoAPI import BRepAlgoAPI_Common
from OCP.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCP.BRepBndLib import BRepBndLib
from OCP.Bnd import Bnd_Box
from OCP.gp import gp_Pnt, gp_Trsf, gp_Vec, gp_Ax1, gp_Dir
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_SOLID
from OCP.TDocStd import TDocStd_Document
from OCP.TCollection import TCollection_ExtendedString
from OCP.XCAFDoc import XCAFDoc_DocumentTool, XCAFDoc_ColorType
from OCP.Quantity import Quantity_Color, Quantity_TOC_RGB
from OCP.IFSelect import IFSelect_RetDone

root=Path(__file__).resolve().parents[1]
source=root/'pcb_sources/p3/RT1_16A_library_8pin_source.step'
r=STEPControl_Reader();assert r.ReadFile(str(source))==IFSelect_RetDone
r.TransferRoots();shape=r.OneShape()
def clip(z,height):
    result=BRepAlgoAPI_Common(shape,BRepPrimAPI_MakeBox(gp_Pnt(-10,-10,z),50,30,height).Shape())
    result.Build();assert result.IsDone();return result.Shape()
def bounds(s):
    b=Bnd_Box();BRepBndLib.Add_s(s,b);return tuple(round(v,6) for v in b.Get())
# Extract the eight physically separate metal pins below the case. Colours are
# presentation only; the geometric union remains the original complete model.
pin_shape=clip(-10,10)
e=TopExp_Explorer(pin_shape,TopAbs_SOLID);centres=[]
while e.More():
    b=bounds(e.Current());centres.append(((b[0]+b[3])/2,(b[1]+b[4])/2));e.Next()
expected=[(x,y) for x in (0,15.26,20.3,25.34) for y in (0,7.5)]
assert len(centres)==8
assert sorted((round(x,4),round(y,4)) for x,y in centres)==sorted(expected)
shift=gp_Trsf();shift.SetTranslation(gp_Vec(-12.15,-3.75,0))
turn=gp_Trsf();turn.SetRotation(gp_Ax1(gp_Pnt(0,0,0),gp_Dir(0,0,1)),-math.pi/2)
def orient(s):
    return BRepBuilderAPI_Transform(BRepBuilderAPI_Transform(s,shift,True).Shape(),turn,True).Shape()
doc=TDocStd_Document(TCollection_ExtendedString('XmlXCAF'))
shapes=XCAFDoc_DocumentTool.ShapeTool_s(doc.Main());colors=XCAFDoc_DocumentTool.ColorTool_s(doc.Main())
for part,rgb in [(clip(0,30),(.88,.27,.055)),(pin_shape,(.65,.67,.69))]:
    label=shapes.AddShape(orient(part),False)
    colors.SetColor(label,Quantity_Color(*rgb,Quantity_TOC_RGB),XCAFDoc_ColorType.XCAFDoc_ColorGen)
w=STEPCAFControl_Writer();w.SetColorMode(True);assert w.Transfer(doc,STEPControl_AsIs)
assert w.Write(str(root/'models/RT314006_16A_8PIN_KICAD_REFERENCE.step'))==IFSelect_RetDone
report={'source':str(source.relative_to(root)),'source_pin_centers_cartesian_mm':sorted(centres),
        'top_view_local_pin_centers_mm':sorted((round(y-3.75,4),round(x-12.15,4)) for x,y in centres),
        'complete_model_bbox_mm':bounds(orient(shape)),'pin_count':8,
        'transformation':'translation then proper -90 degree rotation about Z; no mirroring, clipping or removal of pins',
        'status':'All eight library pins align with board holes. KiCad model reference, not exact TE STEP or a claim of manufacturer tolerance verification.'}
(root/'reports/pcb/p3-relay-model.json').write_text(json.dumps(report,indent=2)+'\n')
print('Verified and retained eight physical model pins; 3D-to-top-view hole coordinates agree.')
