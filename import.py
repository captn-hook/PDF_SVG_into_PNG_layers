#bpy script to import a folder of svg's

import bpy
import os
# to 0
bpy.context.preferences.edit.undo_steps = 0
# to false
bpy.context.preferences.edit.use_global_undo = False

path = "./svg/"
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
        #redraw
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)        
        #save the file to avoid memory overload
        bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
