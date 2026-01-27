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
    LinearizationResult,
    ModelicaSystem,
    ModelicaSystemOMC,
    ModelExecutionCmd,
    ModelicaSystemDoE,
    ModelicaDoEOMC,
    ModelicaSystemError,

    ModelicaSystemRunner,
    ModelicaDoERunner,

    doe_get_solutions,
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
    'ModelicaSystemOMC',
    'ModelExecutionCmd',
    'ModelicaSystemDoE',
    'ModelicaDoEOMC',
    'ModelicaSystemError',

    'ModelicaSystemRunner',
    'ModelicaDoERunner',

    'doe_get_solutions',

    'OMCSessionCmd',
    'OMCSessionException',
    'OMCSessionZMQ',
    'OMCSessionPort',
    'OMCSessionLocal',
    'OMCSessionDocker',
    'OMCSessionDockerContainer',
    'OMCSessionWSL',
]
