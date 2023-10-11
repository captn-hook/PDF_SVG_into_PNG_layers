#a program to convert pdf's with embedded svg's to individual pngs's for each layer
# alias inkscape="flatpak run --command=bash org.inkscape.Inkscape" 

#convert the pdf to svg
flatpak run org.inkscape.Inkscape --export-type=svg -l $1
#svg = $1.svg
svg=$1.svg

#get layer ids
layer_ids=$(flatpak run org.inkscape.Inkscape --query-all $svg | cut -d ',' -f 1)
#remove all ids that start with 'path', 'use', and 'g'
layer_ids=$(echo $layer_ids | sed 's/path[0-9]*//g')
layer_ids=$(echo $layer_ids | sed 's/use[0-9]*//g')
layer_ids=$(echo $layer_ids | sed 's/g[0-9]*//g')

echo $layer_ids
#convert the svg layers to individual pngs using --export-id-only
for id in $layer_ids
do
    flatpak run org.inkscape.Inkscape --export-type=png --export-id-only --export-id=$id --export-filename=$id.png $svg
done

#convert the svg layers to individual pngs
#inkscape --export-type=png --export-id-only --export-id=layer1 --export-filename=layer1.png tmp.svg

#inkscape --export-type=svg --pdf-poppler -l FILENAME.pdf
#inkscape --pdf-page=- $1 --export-type=pdf --export-filename=OUT.pdf --export-area-page
#inkscape --pdf-poppler --pdf-page=1 --export-type=svg --export-text-to-path --export-area-drawing --export-filename tmp2.svg $1
#inkscape -g --batch-process --actions="EditSelectAll;StrokeToPath;export-filename:tmp.svg;export-do;FileClose" tmp2.svg
