# -*- coding: utf-8 -*-
"""
OMPython is a Python interface to OpenModelica.
To get started, create an OMCSessionZMQ object:
from OMPython import OMCSessionZMQ
omc = OMCSessionZMQ()
omc.sendExpression("command")
"""

from OMPython.ModelicaSystem import (
    LinearizationResult,
    ModelicaSystem,
    ModelExecutionCmd,
    ModelicaSystemDoE,
    ModelicaSystemError,
)
from OMPython.OMCSession import (
    ModelExecutionData,
    ModelExecutionException,

    OMCSessionCmd,
    OMCSessionException,
    OMCSessionZMQ,
    OMCSessionPort,
    OMCSessionLocal,
    OMCSessionDocker,
    OMCSessionDockerContainer,
    OMCSessionWSL,
)

# global names imported if import 'from OMPython import *' is used
__all__ = [
    'LinearizationResult',

    'ModelExecutionData',
    'ModelExecutionException',

    'ModelicaSystem',
    'ModelExecutionCmd',
    'ModelicaSystemDoE',
    'ModelicaSystemError',

    'OMCSessionCmd',
    'OMCSessionException',
    'OMCSessionZMQ',
    'OMCSessionPort',
    'OMCSessionLocal',
    'OMCSessionDocker',
    'OMCSessionDockerContainer',
    'OMCSessionWSL',
]
