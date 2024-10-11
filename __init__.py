# Copyright (C) 2019 h0bB1T
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
#
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301  USA

import bpy, platform, os, stat

from . preferences          import PreferencesPanel, T3DN_OT_bip_showcase_install_pillow
from . properties           import TexturesToExport, UI_UL_TexturePackList, Properties
from . preview_parsers      import CollectionImageParser, NodesParser
from . preview_helper       import PreviewHelper
from . panels               import ImportPanel, ExportPanel, NodeWizardPanel, NodeWizardMapPanel, NodeWizardExportPanel
from . create_category_ops  import CreateCategoryOperator
from . exporter_ops         import UseObjectNameOperator, OverwriteObjectExporterOperator, TexturePackSelectionOperator,ObjectExporterOperator
from . importer_ops         import (AppendObjectOperator, LinkObjectOperator, 
                                        SetMaterialOperator, AppendMaterialOperator, OpenObjectOperator, OpenMaterialOperator)
from . render_previews_ops  import ModalTimerOperator, RenderPreviewsOperator, RenderAllPreviewsOperator   
from . generate_ops         import GeneratePBROperator, GenerateImageOperator, ExportPBROperator, ExportMaterialOperator             
from . node_importer_ops    import NodeImporter   
from . ao_curv_calc_ops     import BakeAoMapOperator, CurvatureMapOperator, AoNodeOperator, CurvatureNodeOperator, MapGenerateUV, UseObjectNameForMap
from . tools_ops            import (DX2OGLConverterOperator, GenerateTwoLayerTextureBasedSetupOperator,
                                        GenerateTwoLayerShaderBasedSetupOperator, ImportDistortionOperator,
                                        ImportBlurOperator, ImportTextureBoxMapUVW, ImportExtNoise,
                                        ImportExtMusgrave, ImportExtVoronoi, ImportMixNoise,
                                        ImportScalarMix, ImportIntensityVisualizer, ImportScalarMapper,
                                        ImportNormalDirection, ImportSlice)             
from . support_ops          import AutoNumberExportName, RefreshObjectPreviews, ReRenderObjectPreview, RefreshMaterialPreviews, ReRenderMaterialPreview, RemoveAsset                                        
from . utils                import (categories, categories_enum, ASSET_TYPE_OBJECT, ASSET_TYPE_MATERIAL,
                                        ASSET_TYPE_NODES, ASSET_TYPE_NODES_MATERIALS)
from . icon_helper          import IconHelper


bl_info = {
    "name" : "Asset Wizard",
    "version": (0, 3, 1),
    "author" : "h0bB1T, Atticus",
    "description" : "Asset import and export utility.",
    "blender" : (2, 80, 0),
    "location" : "View3D",
    "category" : "Import-Export"
}

ops = [
    PreferencesPanel,T3DN_OT_bip_showcase_install_pillow,
    TexturesToExport,
    Properties,
    ImportPanel,
    UI_UL_TexturePackList,
    ExportPanel,
    NodeWizardPanel,
    NodeWizardMapPanel,
    NodeWizardExportPanel,
    CreateCategoryOperator,
    UseObjectNameOperator,
    OverwriteObjectExporterOperator,
    TexturePackSelectionOperator,
    ObjectExporterOperator,
    AppendObjectOperator, 
    LinkObjectOperator, 
    SetMaterialOperator, 
    AppendMaterialOperator, 
    OpenObjectOperator,
    OpenMaterialOperator,
    ModalTimerOperator,
    RenderPreviewsOperator,
    RenderAllPreviewsOperator,
    GeneratePBROperator, 
    GenerateImageOperator, 
    ExportPBROperator,
    ExportMaterialOperator,
    NodeImporter,
    BakeAoMapOperator,
    CurvatureMapOperator,
    AoNodeOperator,
    CurvatureNodeOperator,
    UseObjectNameForMap,
    MapGenerateUV,
    DX2OGLConverterOperator, 
    GenerateTwoLayerTextureBasedSetupOperator,
    GenerateTwoLayerShaderBasedSetupOperator, 
    ImportDistortionOperator,
    ImportBlurOperator, 
    ImportTextureBoxMapUVW, 
    ImportExtNoise,
    ImportExtMusgrave, 
    ImportExtVoronoi, 
    ImportMixNoise,
    ImportScalarMix, 
    ImportIntensityVisualizer, 
    ImportScalarMapper,
    ImportNormalDirection, 
    ImportSlice,
    RefreshObjectPreviews,
    ReRenderObjectPreview,
    RefreshMaterialPreviews,
    ReRenderMaterialPreview,
    RemoveAsset,
    AutoNumberExportName,
]

def register():
    for op in ops:
        try:
            bpy.utils.register_class(op)
        except Exception as ex:
            print(ex)
            

    # Prepare previews for node wizard
    for (asset_type, mod) in (
        (ASSET_TYPE_NODES, "nodes"),
        (ASSET_TYPE_NODES_MATERIALS, "materials")
        ):
        PreviewHelper.addCollection(asset_type, NodesParser(), mod)        

    IconHelper.init()

    Properties.initialize()

    # On Linux, guarantee curvature has execute rights.
    if platform.system() == "Linux":
        os.chmod(
            os.path.join(os.path.dirname(__file__), "data", "tools", "curvature"),
            stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH |
            stat.S_IWUSR | stat.S_IWGRP |
            stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
        )

def unregister():
    Properties.cleanup()

    IconHelper.dispose()
    PreviewHelper.removeAllCollections()

    for op in ops:
        try:
            bpy.utils.unregister_class(op)
        except Exception as ex:
            print(ex)


if __name__ == "__main__":
    register()    
