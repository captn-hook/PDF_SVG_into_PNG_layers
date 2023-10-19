this script takes a pdf as an arg and writes out a individual svg for every layer of an embedded svg in it

it uses flatpak inkscape 1.3, but will work with any inkscape 1.3 install if you edit it.

chmod +x convert.sh
chmod +x blender.sh
\
inkscape backpacks-svgrepo-com.svg --batch-process --actions='select-all;path-simplify;export-plain-svg'
sudo flatpak run org.inkscape.Inkscape layer-oc1.svg --batch-process --actions='select-all;path-simplify;export-plain-svg'


scour -i layer-oc1.svg -o TEST.svg