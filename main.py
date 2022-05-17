import os.path

import vtkmodules.all as vtk

INPUT_FILE = "files/vw_knee.slc"
BONE_FILE = "spooky_skeleton.vtk"
BONE_FILE_RANGE = "spooky_skeleton.range"


def get_body_part_contour(reader, value):
    filter = vtk.vtkContourFilter()
    filter.SetInputConnection(reader.GetOutputPort())
    filter.SetValue(0, value)
    return filter


def create_renderer(actors, color):
    renderer = vtk.vtkRenderer()
    for actor in actors:
        renderer.AddActor(actor)
    renderer.SetBackground(color)
    # TODO add box (Maybe at a global level to avoid duplication)
    return renderer


def get_bone_actor(bone_contour):
    bone_mapper = vtk.vtkPolyDataMapper()
    bone_mapper.SetInputConnection(bone_contour.GetOutputPort())
    bone_mapper.ScalarVisibilityOff()


    bone_actor = vtk.vtkActor()
    bone_actor.SetMapper(bone_mapper)
    bone_actor.GetProperty().SetDiffuse(0.8)
    bone_actor.GetProperty().SetDiffuseColor(colors.GetColor3d('Ivory'))
    bone_actor.GetProperty().SetSpecular(0.8)
    bone_actor.GetProperty().SetSpecularPower(120.0)

    return bone_actor


def setup_skin_properties(skin):
    skin.GetProperty().SetDiffuse(0.8)
    skin.GetProperty().SetDiffuseColor(colors.GetColor3d('LightCoral'))
    skin.GetProperty().SetSpecular(0.1)
    skin.GetProperty().SetSpecularPower(120.0)


def get_distance_filter(bone_contour, skin_contour):
    if os.path.isfile(BONE_FILE):
        bone_reader = vtk.vtkPolyDataReader()
        bone_reader.SetFileName(BONE_FILE)
        bone_reader.ReadAllScalarsOn()
        with open(BONE_FILE_RANGE, "r") as file_range:
            exclusion = file_range.readline().split(" ")
            range = (float(exclusion[0]), float(exclusion[1]))
        return bone_reader, range
    else:
        distance_filter = vtk.vtkDistancePolyDataFilter()
        distance_filter.SetInputConnection(0, bone_contour.GetOutputPort())
        distance_filter.SetInputConnection(1, skin_contour.GetOutputPort())
        distance_filter.SignedDistanceOff()
        distance_filter.Update()

        print("Writing")
        writer = vtk.vtkPolyDataWriter()
        writer.SetFileName(BONE_FILE)
        writer.SetFileTypeToBinary()
        writer.SetInputData(distance_filter.GetOutput(0))
        writer.Write()
        with open(BONE_FILE_RANGE, "w") as file_range:
            file_range.write(
                str(distance_filter.GetOutput().GetPointData().GetScalars().GetRange()[0]) +
                " " +
                str(distance_filter.GetOutput().GetPointData().GetScalars().GetRange()[1])
            )

        print("Done writing")
        range = (distance_filter.GetOutput().GetPointData().GetScalars().GetRange()[0],
                 distance_filter.GetOutput().GetPointData().GetScalars().GetRange()[1])
        return distance_filter, range


def get_bone_mapper(bone_contour):
    bone_mapper = vtk.vtkPolyDataMapper()
    bone_mapper.SetInputConnection(bone_contour.GetOutputPort())
    bone_mapper.ScalarVisibilityOff()
    return bone_mapper


def get_bone_data_filtered(bone_contour, skin_contour):
    bone_reader, range = get_distance_filter(bone_contour, skin_contour)
    distance = bone_reader.GetOutputPort(0)

    exclusion = vtk.vtkDoubleArray()
    exclusion.SetNumberOfComponents(2)
    exclusion.SetNumberOfTuples(1)
    exclusion.FillComponent(0, 2.4)
    exclusion.FillComponent(1, float("inf"))

    selection_params = vtk.vtkSelectionNode()
    selection_params.SetContentType(selection_params.THRESHOLDS)
    selection_params.SetFieldType(selection_params.CELL)
    selection_params.SetSelectionList(exclusion)

    selector = vtk.vtkSelection()
    selector.SetNode("cells", selection_params)

    selection = vtk.vtkExtractSelection()
    selection.SetInputConnection(0, distance)
    selection.SetInputData(1, selector)

    # Getting polydata back
    converter = vtk.vtkGeometryFilter()
    converter.SetInputConnection(selection.GetOutputPort())
    converter.Update()
    return converter, range


def upper_left(bone_contour, skin_contour):
    plane = vtk.vtkPlane()
    plane.SetNormal(0, 0, 1)
    plane.SetOrigin(0, 0, 0)
    cutter = vtk.vtkCutter()

    cutter.SetInputConnection(skin_contour.GetOutputPort())
    cutter.SetCutFunction(plane)
    cutter.GenerateValues(25, 0, 300)

    stripper = vtk.vtkStripper()
    stripper.SetInputConnection(cutter.GetOutputPort())

    tube = vtk.vtkTubeFilter()
    tube.SetInputConnection(stripper.GetOutputPort())
    tube.SetRadius(1)

    michel_bone = get_bone_actor(bone_contour)

    skin_mapper = vtk.vtkPolyDataMapper()
    skin_mapper.SetInputConnection(tube.GetOutputPort())
    skin_mapper.ScalarVisibilityOff()

    michel_skin = vtk.vtkActor()
    michel_skin.SetMapper(skin_mapper)
    setup_skin_properties(michel_skin)

    return create_renderer([michel_skin, michel_bone], colors.GetColor3d('LightPink'))


def upper_right(bone_contour, skin_contour):
    sphere = vtk.vtkSphere()
    sphere.SetRadius(50)
    sphere.SetCenter(70, 30, 110)
    clipper = vtk.vtkClipPolyData()
    clipper.SetInputConnection(skin_contour.GetOutputPort())
    clipper.SetClipFunction(sphere)

    michel_bone = get_bone_actor(bone_contour)

    skin_mapper = vtk.vtkPolyDataMapper()
    skin_mapper.SetInputConnection(clipper.GetOutputPort())
    skin_mapper.ScalarVisibilityOff()

    michel_skin = vtk.vtkActor()
    michel_skin.SetMapper(skin_mapper)
    michel_skin.GetProperty().SetOpacity(0.5)
    michel_skin.SetBackfaceProperty(michel_skin.MakeProperty())
    michel_skin.GetBackfaceProperty().SetColor(colors.GetColor3d('LightCoral'))
    setup_skin_properties(michel_skin)

    # TODO add box (Maybe at a global level to avoid duplication)
    return renderer


def lower_left(bone_contour, skin_contour):
    sphere = vtk.vtkSphere()
    sphere.SetRadius(50)
    sphere.SetCenter(70, 30, 110)
    clipper = vtk.vtkClipPolyData()
    clipper.SetInputConnection(skin_contour.GetOutputPort())
    clipper.SetClipFunction(sphere)

    sphere_source = vtk.vtkSphereSource()
    sphere_source.SetRadius(50)
    sphere_source.SetCenter(70, 30, 110)

    sphere_mapper = vtk.vtkPolyDataMapper()
    sphere_mapper.SetInputConnection(sphere_source.GetOutputPort())

    sphere_actor = vtk.vtkActor()
    sphere_actor.SetMapper(sphere_mapper)
    sphere_actor.GetProperty().SetOpacity(0.1)

    michel_bone = get_bone_actor(bone_contour)

    # Skin
    skin_mapper = vtk.vtkPolyDataMapper()
    skin_mapper.SetInputConnection(clipper.GetOutputPort())
    skin_mapper.ScalarVisibilityOff()

    michel_skin = vtk.vtkActor()
    michel_skin.SetMapper(skin_mapper)
    setup_skin_properties(michel_skin)

    # TODO add box (Maybe at a global level to avoid duplication)
    return renderer


def lower_right(bone_contour, skin_contour):
    bone_data, range  = get_bone_data_filtered(bone_contour, skin_contour)
    distance_mapper = vtk.vtkPolyDataMapper()
    distance_mapper.SetInputConnection(bone_data.GetOutputPort())
    distance_mapper.SetScalarRange(
        range[0],
        range[1],
    )

    michel_bone = vtk.vtkActor()
    michel_bone.SetMapper(distance_mapper)
    michel_bone.GetProperty().SetDiffuse(0.8)
    michel_bone.GetProperty().SetSpecular(0.8)
    michel_bone.GetProperty().SetSpecularPower(120.0)

    return create_renderer([michel_bone], colors.GetColor3d('Gainsboro'))


# https://kitware.github.io/vtk-examples/site/Python/IO/ReadSLC/
reader = vtk.vtkSLCReader()
reader.SetFileName(INPUT_FILE)
reader.Update()

colors = vtk.vtkNamedColors()

# Bone
boneContourFilter = get_body_part_contour(reader, 72)

# Skin
skinContourFilter = get_body_part_contour(reader, 50)

renderer1 = upper_left(boneContourFilter, skinContourFilter)
renderer2 = upper_right(boneContourFilter, skinContourFilter)
renderer3 = lower_left(boneContourFilter, skinContourFilter)
renderer4 = lower_right(boneContourFilter, skinContourFilter)

renderer1.SetViewport([0.0, 0.5, 0.5, 1.0])
renderer2.SetViewport([0.5, 0.5, 1.0, 1.0])
renderer3.SetViewport([0.0, 0.0, 0.5, 0.5])
renderer4.SetViewport([0.5, 0.0, 1.0, 0.5])
# Create a rendering window and renderer.
renderWindow = vtk.vtkRenderWindow()
renderWindow.AddRenderer(renderer1)
renderWindow.AddRenderer(renderer2)
renderWindow.AddRenderer(renderer3)
renderWindow.AddRenderer(renderer4)
renderWindow.SetSize(800, 800)

# Create a renderwindowinteractor.
renderWindowInteractor = vtk.vtkRenderWindowInteractor()
renderWindowInteractor.SetRenderWindow(renderWindow)

# Pick a good view
cam1 = renderer1.GetActiveCamera()
cam1.SetPosition(0.0, -1.0, 0.0)
cam1.SetViewUp(0.0, 0.0, -1.0)
renderer1.ResetCamera()
renderer1.ResetCameraClippingRange()

renderer2.SetActiveCamera(cam1)
renderer3.SetActiveCamera(cam1)
renderer4.SetActiveCamera(cam1)

# renderWindow.SetWindowName('ReadSLC')
# renderWindow.SetSize(640, 512)
# renderWindow.Render()

# Enable user interface interactor.
renderWindowInteractor.Initialize()
renderWindow.Render()
renderWindowInteractor.Start()
