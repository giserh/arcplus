'''
Export a folder of maps to PDFs at their Map Document set sizes

Known to work ArcGIS 10.4.1 and Python 2.7.3
Adapted from work by @bteranUFA and @Guest
https://gis.stackexchange.com/questions/7147/how-to-batch-export-mxd-to-pdf-files

License X/MIT; (c) 2017 Environment Yukon, Matt Wilkie
'''

import os
import glob
import arcpy

# Folder to look for MXDs in
in_path = arcpy.GetParameterAsText(0)
# Where to save output documents
exportPath = arcpy.GetParameterAsText(1)
if exportPath == '':
    exportPath = in_path

overwrite = arcpy.GetParameter(2)
arcpy.AddMessage('Overwrite: %s' % overwrite)

# Set the PDF parameters as variables here:
data_frame = 'PAGE_LAYOUT'  # PAGE_LAYOUT or dataframe name
df_export_width = 1920      # ignored when using PAGE_LAYOUT
df_export_height = 1200
resolution = '300'
image_quality = 'BEST'      # FASTEST, FASTER, NORMAL, BETTER, BEST
colorspace = 'RGB'          # RGB, CMYK
compress_vectors = 'True'
image_compression = 'ADAPTIVE'      # ADAPTIVE, JPEG, DEFLATE, LZW, RLE, NONE
picture_symbol = 'VECTORIZE_BITMAP' # RASTERIZE_BITMAP, RASTERIZE_PICTURE, VECTORIZE_BITMAP
convert_markers = 'False'
embed_fonts = 'True'
layers_attributes = 'LAYERS_ONLY'   # LAYERS_ONLY, LAYERS_AND_ATTRIBUTES, NONE
georef_info = 'True'
jpeg_compression_quality = 85

maps = glob.glob(os.path.join(in_path, '*.mxd'))

def exportmap(mxdPath, exportPath):
    fname = os.path.split(mxdPath)[1]                    # ''some_map.mxd' - discard prefix path elements
    basename = os.path.splitext(fname)[0]                # 'some_map' - discard extension
    newPDF = os.path.join(exportPath, basename + '.pdf') # 'Y:\output\some_map.pdf'
    open(newPDF, 'w').close()   # create empty marker file , for parallel script running.

    arcpy.AddMessage('Reading: ' + m)
    mxd = arcpy.mapping.MapDocument(m)
    arcpy.AddMessage('Writing: ' + newPDF)
    arcpy.mapping.ExportToPDF(mxd, newPDF, data_frame, df_export_width, df_export_height, resolution, image_quality,
                              colorspace, compress_vectors, image_compression, picture_symbol, convert_markers, embed_fonts,
                              layers_attributes, georef_info, jpeg_compression_quality)
    del mxd
    return

for m in maps:
    fname = os.path.split(m)[1]                          # ''some_map.mxd' - discard prefix path elements
    basename = os.path.splitext(fname)[0]                # 'some_map' - discard extension
    newPDF = os.path.join(exportPath, basename + '.pdf') # 'Y:\output\some_map.pdf'
    arcpy.AddMessage('--- %s' % os.path.split(m)[1])

    if os.path.exists(newPDF):
        if overwrite == True:
            exportmap(m, newPDF)
        else:
            arcpy.AddMessage('Skipping %s' % newPDF)


arcpy.GetMessages()