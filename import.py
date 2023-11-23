# bpy script to import a folder of svg's

path = "/home/hook/PDF_SVG_into_PNG_layers/test/Layerd/Sunstone/"

import bpy
import os

def get_layer_collection(collection, view_layer=None):
    """Returns the view layer LayerCollection for a specificied Collection"""

    def scan_children(lc, result=None):
        for c in lc.children:
            if c.collection == collection:
                return c
            result = scan_children(c, result)
        return result

    if view_layer is None:
        view_layer = bpy.context.view_layer
    return scan_children(view_layer.layer_collection)

# to 0
bpy.context.preferences.edit.undo_steps = 0
# to false
bpy.context.preferences.edit.use_global_undo = False


def rec_join_col(collection):
    # joins all objects in collection into one object, but only n at a time to avoid memory overload
    objs = collection.objects
    for o in objs:
        o.select_set(True)
        # set active object to last selected
        bpy.context.view_layer.objects.active = o
        if len(bpy.context.selected_objects) > 300:
            bpy.ops.object.join()


files = os.listdir(path)
# sort files by name and number
files.sort(key=lambda f: int("".join(filter(str.isdigit, f))))
print(files)
i = 0
for f in files:
    i += 1
    print(i, f)
    # if svg and collection of same name doesn't exist
    if f.endswith(".svg") and f not in bpy.data.collections:
        bpy.ops.import_curve.svg(filepath=path + f)
        # curves will be imported into a new collection
        col = bpy.data.collections[-1]
        # remove all materials on all objects in collection, then join curves into one object
        bpy.ops.object.select_all(action="DESELECT")
        for obj in col.objects:
            mat = obj.active_material
            if mat:
                # mat.user_clear()
                bpy.data.materials.remove(mat)

        rec_join_col(col)

        # exclude the collection from layer render
        # lc = get_layer_collection(col)
        # #exclude col from lc
        # lc.exclude = True
        # redraw
        # bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
        # save the file to avoid memory overload
        bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)

