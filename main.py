import vtkmodules.all as vtk

input_file = "files/vw_knee.slc"


def get_body_part_contour(reader, value):
    filter = vtk.vtkContourFilter()
    filter.SetInputConnection(reader.GetOutputPort())
    # Change the range(2nd and 3rd Paramater) based on your
    # requirement. recomended value for 1st parameter is above 1
    filter.SetValue(0, value)
    return filter


def upper_left(bone_contour, skin_contour):
    plane = vtk.vtkPlane()
    plane.SetNormal(0, 0, 1)
    plane.SetOrigin(0, 0, 0)
    cutter = vtk.vtkCutter()
    cutter.SetInputConnection(skin_contour.GetOutputPort())
    cutter.SetCutFunction(plane)
    cutter.GenerateValues(25, 0, 300)

    boneMapper = vtk.vtkPolyDataMapper()
    boneMapper.SetInputConnection(bone_contour.GetOutputPort())
    boneMapper.ScalarVisibilityOff()

    # Skin
    skinMapper = vtk.vtkPolyDataMapper()
    skinMapper.SetInputConnection(cutter.GetOutputPort())
    skinMapper.ScalarVisibilityOff()

    michelBone = vtk.vtkActor()
    michelBone.SetMapper(boneMapper)
    michelBone.GetProperty().SetDiffuse(0.8)
    michelBone.GetProperty().SetDiffuseColor(colors.GetColor3d('Ivory'))
    michelBone.GetProperty().SetSpecular(0.8)
    michelBone.GetProperty().SetSpecularPower(120.0)

    michelSkin = vtk.vtkActor()
    michelSkin.SetMapper(skinMapper)
    michelSkin.GetProperty().SetDiffuse(0.8)
    michelSkin.GetProperty().SetDiffuseColor(colors.GetColor3d('LightCoral'))
    michelSkin.GetProperty().SetSpecular(0.1)
    michelSkin.GetProperty().SetSpecularPower(120.0)

    renderer = vtk.vtkRenderer()
    renderer.AddActor(michelBone)
    renderer.AddActor(michelSkin)
    renderer.SetBackground(colors.GetColor3d('LightPink'))
    # TODO add box (Maybe at a global level to avoid duplication)
    return renderer


def upper_right(bone_contour, skin_contour):
    sphere = vtk.vtkSphere()
    sphere.SetRadius(50)
    sphere.SetCenter(70, 30, 110)
    clipper = vtk.vtkClipPolyData()
    clipper.SetInputConnection(skin_contour.GetOutputPort())
    clipper.SetClipFunction(sphere)

    boneMapper = vtk.vtkPolyDataMapper()
    boneMapper.SetInputConnection(bone_contour.GetOutputPort())
    boneMapper.ScalarVisibilityOff()

    # Skin
    skinMapper = vtk.vtkPolyDataMapper()
    skinMapper.SetInputConnection(clipper.GetOutputPort())
    skinMapper.ScalarVisibilityOff()

    michelBone = vtk.vtkActor()
    michelBone.SetMapper(boneMapper)
    michelBone.GetProperty().SetDiffuse(0.8)
    michelBone.GetProperty().SetDiffuseColor(colors.GetColor3d('Ivory'))
    michelBone.GetProperty().SetSpecular(0.8)
    michelBone.GetProperty().SetSpecularPower(120.0)

    michelSkin = vtk.vtkActor()
    michelSkin.SetMapper(skinMapper)
    michelSkin.GetProperty().SetOpacity(0.5)
    michelSkin.SetBackfaceProperty(michelSkin.MakeProperty())
    michelSkin.GetBackfaceProperty().SetColor(colors.GetColor3d('LightCoral'))
    michelSkin.GetProperty().SetDiffuse(0.8)
    michelSkin.GetProperty().SetDiffuseColor(colors.GetColor3d('LightCoral'))
    michelSkin.GetProperty().SetSpecular(0.1)
    michelSkin.GetProperty().SetSpecularPower(120.0)

    renderer = vtk.vtkRenderer()
    renderer.AddActor(michelBone)
    renderer.AddActor(michelSkin)
    renderer.SetBackground(colors.GetColor3d('PaleGreen'))
    # TODO add box (Maybe at a global level to avoid duplication)
    return renderer

def lower_left(bone_contour, skin_contour):
    sphere = vtk.vtkSphere()
    sphere.SetRadius(50)
    sphere.SetCenter(70, 30, 110)
    clipper = vtk.vtkClipPolyData()
    clipper.SetInputConnection(skin_contour.GetOutputPort())
    clipper.SetClipFunction(sphere)

    # TODO ask if must be the same sphere or can use a new one
    sphere_source = vtk.vtkSphereSource()
    sphere_source.SetRadius(50)
    sphere_source.SetCenter(70, 30, 110)

    sphere_mapper = vtk.vtkPolyDataMapper()
    sphere_mapper.SetInputConnection(sphere_source.GetOutputPort())

    sphere_actor = vtk.vtkActor()
    sphere_actor.SetMapper(sphere_mapper)
    sphere_actor.GetProperty().SetOpacity(0.1)

    boneMapper = vtk.vtkPolyDataMapper()
    boneMapper.SetInputConnection(bone_contour.GetOutputPort())
    boneMapper.ScalarVisibilityOff()

    # Skin
    skinMapper = vtk.vtkPolyDataMapper()
    skinMapper.SetInputConnection(clipper.GetOutputPort())
    skinMapper.ScalarVisibilityOff()

    michelBone = vtk.vtkActor()
    michelBone.SetMapper(boneMapper)
    michelBone.GetProperty().SetDiffuse(0.8)
    michelBone.GetProperty().SetDiffuseColor(colors.GetColor3d('Ivory'))
    michelBone.GetProperty().SetSpecular(0.8)
    michelBone.GetProperty().SetSpecularPower(120.0)

    michelSkin = vtk.vtkActor()
    michelSkin.SetMapper(skinMapper)
    michelSkin.GetProperty().SetDiffuse(0.8)
    michelSkin.GetProperty().SetDiffuseColor(colors.GetColor3d('LightCoral'))
    michelSkin.GetProperty().SetSpecular(0.1)
    michelSkin.GetProperty().SetSpecularPower(120.0)

    renderer = vtk.vtkRenderer()
    renderer.AddActor(michelBone)
    renderer.AddActor(michelSkin)
    renderer.AddActor(sphere_actor)
    renderer.SetBackground(colors.GetColor3d('LightCyan'))
    # TODO add box (Maybe at a global level to avoid duplication)
    return renderer


def lower_right(bone_contour, skin_contour):
    color_table = vtk.vtkColorTransferFunction()
    color_table.AddRGBPoint(0, 0.52, 0.5, 1)
    color_table.AddRGBPoint(1, 0.129, 0.643, 0.318)
    color_table.AddRGBPoint(400, 0.573, 0.765, 0.431)
    color_table.AddRGBPoint(800, 0.949, 0.864, 0.808)
    color_table.AddRGBPoint(1600, 1, 1, 1)

    distanceFilter = vtk.vtkDistancePolyDataFilter()
    distanceFilter.SetInputConnection(0, bone_contour.GetOutputPort())
    distanceFilter.SetInputConnection(1, skin_contour.GetOutputPort())
    distanceFilter.Update()

    test = vtk.vtkPolyDataMapper()
    test.SetInputConnection(distanceFilter.GetOutputPort())
    test.SetScalarRange(distanceFilter.GetOutput().GetPointData().GetScalars().GetRange()[0],distanceFilter.GetOutput().GetPointData().GetScalars().GetRange()[1])


    boneMapper = vtk.vtkPolyDataMapper()
    boneMapper.SetInputConnection(bone_contour.GetOutputPort())
    boneMapper.ScalarVisibilityOff()
    boneMapper.SetLookupTable(color_table)

    michelBone = vtk.vtkActor()
    michelBone.SetMapper(test)
    michelBone.GetProperty().SetDiffuse(0.8)
    #michelBone.GetProperty().SetDiffuseColor(colors.GetColor3d('Ivory'))
    michelBone.GetProperty().SetSpecular(0.8)
    michelBone.GetProperty().SetSpecularPower(120.0)

    renderer = vtk.vtkRenderer()
    renderer.AddActor(michelBone)
    renderer.SetBackground(colors.GetColor3d('Gainsboro'))

# https://kitware.github.io/vtk-examples/site/Python/IO/ReadSLC/
reader = vtk.vtkSLCReader()
reader.SetFileName(input_file)
reader.Update()

colors = vtk.vtkNamedColors()

# Bone
boneContourFilter = get_body_part_contour(reader, 72)

# Skin
skinContourFilter = get_body_part_contour(reader, 50)

# distanceFilter = vtk.vtkDistancePolyDataFilter()
# distanceFilter.SetInputConnection(0, boneContourFilter)
# distanceFilter.SetInputConnection(1, skinContourFilter)
# distanceFilter.Update()
# distanceFilter.SignedDistanceOff()
#
# distance = vtk.vtkFloatArray()
# distance.SetNumberOfComponents(2)
# distance.SetNumberOfTuples(1)
# distance.FillComponent(0, 5)
# distance.FillComponent(1, float("inf"))


# Create a rendering window and renderer.
renderer = lower_right(boneContourFilter, skinContourFilter)
renderWindow = vtk.vtkRenderWindow()
renderWindow.AddRenderer(renderer)
renderWindow.SetSize(500, 500)

# Create a renderwindowinteractor.
renderWindowInteractor = vtk.vtkRenderWindowInteractor()
renderWindowInteractor.SetRenderWindow(renderWindow)

# Pick a good view
cam1 = renderer.GetActiveCamera()
cam1.SetFocalPoint(0.0, 0.0, 0.0)
cam1.SetPosition(0.0, -1.0, 0.0)
cam1.SetViewUp(0.0, 0.0, -1.0)
cam1.Azimuth(-90.0)
renderer.ResetCamera()
renderer.ResetCameraClippingRange()

renderWindow.SetWindowName('ReadSLC')
renderWindow.SetSize(640, 512)
renderWindow.Render()

# Enable user interface interactor.
renderWindowInteractor.Initialize()
renderWindow.Render()
renderWindowInteractor.Start()
