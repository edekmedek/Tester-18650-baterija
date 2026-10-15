"""Blender CPU rendering of the actual KiCad 10 GLB export (no invented bodies)."""
import bpy
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
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=96
scene.cycles.use_denoising=False
scene.render.resolution_x=1800;scene.render.resolution_y=2000;scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG';scene.render.film_transparent=False
scene.world.color=(.05,.05,.05)
scene.view_settings.exposure=-1
scene.view_settings.view_transform='AgX'
# Graphic refdes labels sit above the non-physical annotation plates so the
# rendering cannot be mistaken for fitted, unidentified component packages.
import json
placement=json.loads((root/'reports/pcb/placement-map.json').read_text())['placements']
labels={'J1':'J1\nNodeMCU CH340\nREFERENCE / FIT TBD',
        'K1':'K1\nRT314006\nPACKAGE TBD',
        'Q1':'Q1\nC3209\nPINOUT TBD',
        'R1':'R1\n22 ohm / 5 W\nPACKAGE TBD',
        'R2':'R2\n22 ohm / 5 W\nPACKAGE TBD',
        'R3':'R3\n10k\nTBD','R4':'R4\n20k\nTBD',
        'BTH1':'BTH1\n18650 HOLDER\nALLOCATION ONLY'}
for ref,caption in labels.items():
    _,x,y=placement[ref]
    curve=bpy.data.curves.new(ref+' graphical label','FONT');curve.body=caption
    curve.align_x='CENTER';curve.align_y='CENTER';curve.size=.00135 if ref not in ('R3','R4') else .001
    obj=bpy.data.objects.new(ref+' NON-PHYSICAL annotation',curve);scene.collection.objects.link(obj)
    obj.location=(x/1000,-y/1000,.0019)
    ink=bpy.data.materials.new(ref+' ink');ink.diffuse_color=((.9,.95,1,1) if ref=='J1' else (.025,.018,.012,1))
    curve.materials.append(ink)
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
scene.render.filepath=str(root/'tester18650_pcb_3d.png')
bpy.ops.wm.save_as_mainfile(filepath='/tmp/tester18650-render.blend')
bpy.ops.render.render(write_still=True)
