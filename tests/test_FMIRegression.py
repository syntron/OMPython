import tempfile
import pathlib
import pytest
import shutil
import os

import OMPython


def buildModelFMU(modelName):
    omc = OMPython.OMCSessionZMQ()

    tempdir = pathlib.Path(tempfile.mkdtemp())
    try:
        omc.sendExpression(f'cd("{tempdir.as_posix()}")')

        omc.sendExpression("loadModel(Modelica)")
        omc.sendExpression("getErrorString()")

        fileNamePrefix = modelName.split(".")[-1]
        exp = f'buildModelFMU({modelName}, fileNamePrefix="{fileNamePrefix}")'
        fmu = omc.sendExpression(exp)
        assert os.path.exists(fmu)
    finally:
        del omc
        shutil.rmtree(tempdir, ignore_errors=True)


def test_Modelica_Blocks_Examples_Filter():
    buildModelFMU("Modelica.Blocks.Examples.Filter")


@pytest.mark.skip("takes too long")
def test_Modelica_Blocks_Examples_RealNetwork1():
    buildModelFMU("Modelica.Blocks.Examples.RealNetwork1")


@pytest.mark.skip("takes too long")
def test_Modelica_Electrical_Analog_Examples_CauerLowPassAnalog():
    buildModelFMU("Modelica.Electrical.Analog.Examples.CauerLowPassAnalog")


@pytest.mark.skip("takes too long")
def test_Modelica_Electrical_Digital_Examples_FlipFlop():
    buildModelFMU("Modelica.Electrical.Digital.Examples.FlipFlop")


@pytest.mark.skip("takes too long")
def test_Modelica_Mechanics_Rotational_Examples_FirstGrounded():
    buildModelFMU("Modelica.Mechanics.Rotational.Examples.FirstGrounded")


@pytest.mark.skip("takes too long")
def test_Modelica_Mechanics_Rotational_Examples_CoupledClutches():
    buildModelFMU("Modelica.Mechanics.Rotational.Examples.CoupledClutches")


@pytest.mark.skip("takes too long")
def test_Modelica_Mechanics_MultiBody_Examples_Elementary_DoublePendulum():
    buildModelFMU("Modelica.Mechanics.MultiBody.Examples.Elementary.DoublePendulum")


@pytest.mark.skip("takes too long")
def test_Modelica_Mechanics_MultiBody_Examples_Elementary_FreeBody():
    buildModelFMU("Modelica.Mechanics.MultiBody.Examples.Elementary.FreeBody")


@pytest.mark.skip("takes too long")
def test_Modelica_Fluid_Examples_PumpingSystem():
    buildModelFMU("Modelica.Fluid.Examples.PumpingSystem")


@pytest.mark.skip("takes too long")
def test_Modelica_Fluid_Examples_TraceSubstances_RoomCO2WithControls():
    buildModelFMU("Modelica.Fluid.Examples.TraceSubstances.RoomCO2WithControls")


@pytest.mark.skip("takes too long")
def test_Modelica_Clocked_Examples_SimpleControlledDrive_ClockedWithDiscreteTextbookController():
    buildModelFMU("Modelica.Clocked.Examples.SimpleControlledDrive.ClockedWithDiscreteTextbookController")
