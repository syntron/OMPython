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
    ModelicaSystemABC,
    ModelicaSystem,
    ModelicaSystemOMC,
    ModelExecutionCmd,
    ModelicaSystemDoE,
    ModelicaDoEOMC,
    ModelicaSystemError,
    ModelicaSystemRunner,

    doe_get_solutions,

    ModelicaSystemCmd,
)
from OMPython.OMCSession import (
    ModelExecutionData,
    ModelExecutionException,

    OMSessionABC,

    OMCSessionCmd,
    OMCSessionException,
    OMCSessionZMQ,
    OMCSessionPort,
    OMCSessionLocal,

    OMCPath,
    OMPathRunnerBash,
    OMPathRunnerLocal,

    OMCSessionABC,
    OMCSessionDocker,
    OMCSessionDockerContainer,
    OMSessionRunner,
    OMCSessionWSL,

    OMCProcessLocal,
    OMCProcessPort,
    OMCProcessDocker,
    OMCProcessDockerContainer,
)

# global names imported if import 'from OMPython import *' is used
__all__ = [
    'LinearizationResult',

    'ModelicaSystemABC',
    'ModelExecutionData',
    'ModelExecutionException',

    'ModelicaSystem',  # compatibility layer
    'ModelicaSystemOMC',
    'ModelExecutionCmd',
    'ModelicaSystemDoE',
    'ModelicaDoEOMC',
    'ModelicaSystemError',
    'ModelicaSystemRunner',

    'ModelicaSystemCmd',

    'doe_get_solutions',

    'OMSessionABC',

    'OMCSessionCmd',  # obsolete
    'OMCSessionException',
    'OMCSessionZMQ',  # compatibility layer
    'OMCSessionPort',
    'OMCSessionLocal',

    'OMCPath',
    'OMPathRunnerBash',
    'OMPathRunnerLocal',

    'OMSessionRunner',

    'OMCSessionABC',
    'OMCSessionDocker',
    'OMCSessionDockerContainer',
    'OMCSessionWSL',

    'OMCProcessLocal',
    'OMCProcessPort',
    'OMCProcessDocker',
    'OMCProcessDockerContainer',
]
