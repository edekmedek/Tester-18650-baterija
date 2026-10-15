#!/usr/bin/env python3
"""Remove only the unpopulated screw terminal visible as absent in the photo.
All remaining geometry comes unchanged from the manufacturer's STEP source.
"""
import json
from pathlib import Path
from OCP.STEPControl import STEPControl_Reader,STEPControl_Writer,STEPControl_AsIs
from OCP.TopAbs import TopAbs_SOLID
from OCP.TopExp import TopExp_Explorer
from OCP.Bnd import Bnd_Box
from OCP.BRepBndLib import BRepBndLib
from OCP.BRep import BRep_Builder
from OCP.TopoDS import TopoDS_Compound
from OCP.IFSelect import IFSelect_RetDone
root=Path(__file__).resolve().parents[1]
r=STEPControl_Reader();assert r.ReadFile(str(root/'pcb_sources/Soldered_INA219_source.step'))==IFSelect_RetDone
r.TransferRoots();e=TopExp_Explorer(r.OneShape(),TopAbs_SOLID)
compound=TopoDS_Compound();builder=BRep_Builder();builder.MakeCompound(compound)
removed=[];kept=0
while e.More():
    shape=e.Current();b=Bnd_Box();BRepBndLib.Add_s(shape,b);bounds=b.Get()
    # The unique large terminal body at the manufacturer K1 location. This
    # selection is validated against the source; it is not an inferred wire/pin.
    if bounds[0]>25 and bounds[3]>38 and bounds[5]>16:
        removed.append(bounds)
    else:builder.Add(compound,shape);kept+=1
    e.Next()
assert len(removed)==1 and kept==28,(removed,kept)
w=STEPControl_Writer();w.Transfer(compound,STEPControl_AsIs)
assert w.Write(str(root/'models/Soldered_INA219_photo_variant.step'))==IFSelect_RetDone
(root/'reports/pcb/ina-model-adaptation.json').write_text(json.dumps({'source':'pcb_sources/Soldered_INA219_source.step','kept_original_solids':kept,'removed_solids':removed,'reason':'Optional screw terminal absent in user top photo. No replacement dimensions or geometry created.'},indent=2)+'\n')
