# -*- coding: utf-8 -*-
"""
OMPython is a Python interface to OpenModelica.
To get started on a local OMC server, create an OMCSessionLocal object:

```
import OMPython
omc = OMPython.OMCSessionLocal()
omc.sendExpression("command")
```

"""

from OMPython.ModelicaSystem import (
    ModelExecutionCmd,

    LinearizationResult,
    ModelicaSystemBase,
    ModelicaSystemError,
    ModelicaSystemOMC,
    ModelicaSystemDoE,
    ModelicaSystemRunner,
)
from OMPython.OMCSession import (
    ModelExecutionData,
    ModelExecutionException,

    OMCSessionException,

    OMCSessionZMQ,

    OMCPath,
    OMCPathDummy,

    OMCSession,
    OMCSessionDocker,
    OMCSessionDockerContainer,
    SessionRunner,
    OMCSessionLocal,
    OMCSessionPort,
    OMCSessionWSL,

    OMCSessionCmd,
)

# compatibility layer
ModelicaSystem = ModelicaSystemOMC

# global names imported if import 'from OMPython import *' is used
__all__ = [
    'LinearizationResult',

    'ModelicaSystemBase',
    'ModelExecutionData',
    'ModelExecutionException',

    'ModelicaSystem',  # compatibility layer
    'ModelExecutionCmd',
    'ModelicaSystemDoE',
    'ModelicaSystemError',
    'ModelicaSystemOMC',
    'ModelicaSystemRunner',

    'ModelExecutionCmd',
    'ModelExecutionData',
    'ModelExecutionException',

    'SessionRunner',

    'OMCSessionException',

    'OMCPath',
    'OMCPathDummy',

    'OMCSessionCmd',  # obsolete
    'OMCSessionZMQ',  # compatibility layer

    'OMCSession',
    'OMCSessionDocker',
    'OMCSessionDockerContainer',
    'OMCSessionLocal',
    'OMCSessionPort',
    'OMCSessionWSL',
]
