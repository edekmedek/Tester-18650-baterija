#!/usr/bin/env python3
"""Create coloured CAD annotation plates. They are not component body models."""
import json
from pathlib import Path
from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCP.gp import gp_Pnt
from OCP.TDocStd import TDocStd_Document
from OCP.TCollection import TCollection_ExtendedString
from OCP.XCAFDoc import XCAFDoc_DocumentTool, XCAFDoc_ColorType
from OCP.Quantity import Quantity_Color, Quantity_TOC_RGB
from OCP.STEPCAFControl import STEPCAFControl_Writer
from OCP.STEPControl import STEPControl_AsIs
from OCP.IFSelect import IFSelect_RetDone

folder=Path(__file__).resolve().parents[1]/'models'
for name,a in json.loads((folder/'marker-geometry.json').read_text()).items():
    assert a['physical_package'] is False
    w,h=a['width'],a['height']
    shape=BRepPrimAPI_MakeBox(gp_Pnt(-w/2,-h/2+a['center_y'],0),w,h,a['graphic_thickness']).Shape()
    doc=TDocStd_Document(TCollection_ExtendedString('XmlXCAF'))
    shapes=XCAFDoc_DocumentTool.ShapeTool_s(doc.Main());label=shapes.AddShape(shape,False)
    colors=XCAFDoc_DocumentTool.ColorTool_s(doc.Main())
    colors.SetColor(label,Quantity_Color(*a['color'],Quantity_TOC_RGB),XCAFDoc_ColorType.XCAFDoc_ColorGen)
    writer=STEPCAFControl_Writer();writer.SetColorMode(True)
    assert writer.Transfer(doc,STEPControl_AsIs)
    assert writer.Write(str(folder/(name+'.step')))==IFSelect_RetDone
print('CAD annotation plates created. 0.02 mm is graphical thickness, not a package dimension.')
