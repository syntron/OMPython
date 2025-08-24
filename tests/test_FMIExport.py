import OMPython
import shutil
import os


def test_CauerLowPassAnalog():
    mod = OMPython.ModelicaSystem()
    mod.definition(
        model="Modelica.Electrical.Analog.Examples.CauerLowPassAnalog",
        libraries=["Modelica"],
    )
    tmp = mod.getWorkDirectory()
    try:
        fmu = mod.convertMo2Fmu(fileNamePrefix="CauerLowPassAnalog")
        assert os.path.exists(fmu)

        # TODO: check if solution is identical to original simulation?!
        mod2 = OMPython.ModelicaSystem()
        mod2.convertFmu2Mo(
            fmu=fmu,
        )

    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_DrumBoiler():
    mod = OMPython.ModelicaSystem()
    mod.definition(
        model="Modelica.Fluid.Examples.DrumBoiler.DrumBoiler",
        libraries=["Modelica"],
    )
    tmp = mod.getWorkDirectory()
    try:
        fmu = mod.convertMo2Fmu(fileNamePrefix="DrumBoiler")
        assert os.path.exists(fmu)

        # TODO: check if solution is identical to original simulation?!
        mod2 = OMPython.ModelicaSystem()
        mod2.convertFmu2Mo(
            fmu=fmu,
        )

    finally:
        shutil.rmtree(tmp, ignore_errors=True)
