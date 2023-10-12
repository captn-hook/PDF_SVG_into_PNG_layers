#bpy script to import a folder of svg's

path = "./svg/"

import bpy
import os
# to 0
bpy.context.preferences.edit.undo_steps = 0
# to false
bpy.context.preferences.edit.use_global_undo = False

def select_collection_objects(collection):
    for obj in collection.all_objects:
        obj.select_set(True)
    #set active object to last selected
    bpy.context.view_layer.objects.active = obj

files = os.listdir(path)
#sort files by name and number
files.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
print(files)
i=0
for f in files:
    i+=1
    print(i, f)
    #if svg and collection of same name doesn't exist
    if f.endswith('.svg') and f not in bpy.data.collections:
        bpy.ops.import_curve.svg(filepath=path+f)
        #curves will be imported into a new collection
        col = bpy.data.collections[-1]
        #remove all materials on all objects in collection, then join curves into one object
        bpy.ops.object.select_all(action='DESELECT')
        for obj in col.objects:
            mat = obj.active_material
            if mat:
                mat.user_clear()
                bpy.data.materials.remove(mat)

        select_collection_objects(col)

        bpy.ops.object.join()
        
        #redraw
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)        
        #save the file to avoid memory overload
        bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
