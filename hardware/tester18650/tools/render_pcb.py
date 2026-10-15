"""Blender CPU rendering of the actual KiCad 10 GLB export (no invented bodies)."""
import bpy
import os
from mathutils import Vector
from pathlib import Path

root=Path(__file__).resolve().parents[1]
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
bpy.ops.import_scene.gltf(filepath=str(root/'tester18650_pcb_3d.glb'))
meshes=[o for o in bpy.context.scene.objects if o.type=='MESH']
coords=[o.matrix_world @ Vector(c) for o in meshes for c in o.bound_box]
lo=Vector(tuple(min(p[i] for p in coords) for i in range(3)))
hi=Vector(tuple(max(p[i] for p in coords) for i in range(3)))
print('Actual imported KiCad GLB bounds in metres:',tuple(lo),tuple(hi))
center=(lo+hi)/2;span=max(hi.x-lo.x,hi.y-lo.y)
# Native GLB keeps the CAD materials, including the amber non-physical markers.
preview=os.environ.get('TESTER_RENDER_PREVIEW')=='1'
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=12 if preview else 96
scene.cycles.use_denoising=False
scene.render.resolution_x=900 if preview else 1800;scene.render.resolution_y=1000 if preview else 2000;scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG';scene.render.film_transparent=False
scene.world.color=(.05,.05,.05)
scene.view_settings.exposure=-1
scene.view_settings.view_transform='AgX'
# Graphic refdes labels sit above the non-physical annotation plates so the
# rendering cannot be mistaken for fitted, unidentified component packages.
import json
placement=json.loads((root/'reports/pcb/placement-map.json').read_text())['placements']
labels={'J1':'J1\nNodeMCU CH340\nREFERENCE / MODEL TBD',
        'K1':'K1 / RT314006\nBODY REFERENCE\nPIN MAP TBD',
        'R1':'R1\n22R / 5W\nALT',
        'R2':'R2\n22R / 5W\nALT'}
label_z={'K1':.0175,'R1':.0295,'R2':.0295}
for ref,caption in labels.items():
    _,x,y=placement[ref]
    curve=bpy.data.curves.new(ref+' graphical label','FONT');curve.body=caption
    curve.align_x='CENTER';curve.align_y='CENTER';curve.size=.0009 if ref in ('R1','R2') else .00125
    obj=bpy.data.objects.new(ref+' NON-PHYSICAL annotation',curve);scene.collection.objects.link(obj)
    obj.location=(x/1000,-(y-3.81 if ref in ('R1','R2') else y)/1000,label_z.get(ref,.0019))
    ink=bpy.data.materials.new(ref+' ink');ink.diffuse_color=((.9,.95,1,1) if ref=='J1' else (.025,.018,.012,1))
    curve.materials.append(ink)
# Renderer-only figure captions describe the references without pretending
# that labels are physical component markings or manufacturing verification.
for caption,x,y,size in [
    ('P2 / PARTIAL PCB - NOT FOR FABRICATION',58,-7,.0022),
    ('Orange: relay body reference. White: proposed resistor substitute.',58,140,.00135),
    ('Black: reference holder. Blue: NodeMCU graphic, model unresolved.',58,143,.00135)]:
    curve=bpy.data.curves.new('Figure caption','FONT');curve.body=caption
    curve.align_x='CENTER';curve.align_y='CENTER';curve.size=size
    obj=bpy.data.objects.new('Non-physical figure caption',curve);scene.collection.objects.link(obj)
    obj.location=(x/1000,-y/1000,.0019)
    mat=bpy.data.materials.new('Caption white');mat.diffuse_color=(.95,.95,.95,1);curve.materials.append(mat)
# Matte background and soft lights for reading the actual layout.
bpy.ops.mesh.primitive_plane_add(size=span*12,location=(center.x,center.y,lo.z-span*.04))
floor=bpy.context.object;floor.name='Studio background (not a board component)'
mat=bpy.data.materials.new('Studio neutral');mat.diffuse_color=(.09,.105,.13,1);mat.use_nodes=True
mat.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.09,.105,.13,1)
mat.node_tree.nodes.get('Principled BSDF').inputs['Roughness'].default_value=.85
floor.data.materials.append(mat)
for i,(relative,power,size) in enumerate([((-1,-1,2.5),2,2),((1.5,.8,2),1.25,1.5),((-.5,2,1.5),.6,1)]):
    lamp=bpy.data.lights.new('Softbox '+str(i),'AREA');lamp.energy=power;lamp.shape='DISK';lamp.size=span*size
    obj=bpy.data.objects.new(lamp.name,lamp);scene.collection.objects.link(obj)
    obj.location=center+Vector(relative)*span;obj.rotation_euler=(center-obj.location).to_track_quat('-Z','Y').to_euler()
cam_data=bpy.data.cameras.new('PCB inspection');cam=bpy.data.objects.new(cam_data.name,cam_data);scene.collection.objects.link(cam)
cam.location=center+Vector((span*.05,-span*1.1,span*2.35));cam.rotation_euler=(center-cam.location).to_track_quat('-Z','Y').to_euler()
cam_data.type='ORTHO';cam_data.ortho_scale=span*1.35;cam_data.lens=50;cam_data.clip_start=.0001;cam_data.clip_end=100
scene.camera=cam
scene.render.filepath='/tmp/tester18650-p2-preview.png' if preview else str(root/'tester18650_pcb_3d.png')
bpy.ops.wm.save_as_mainfile(filepath='/tmp/tester18650-render.blend')
bpy.ops.render.render(write_still=True)
