# -*- coding: utf-8 -*-
"""
Definition of an OMC session.
"""

__license__ = """
 This file is part of OpenModelica.

 Copyright (c) 1998-CurrentYear, Open Source Modelica Consortium (OSMC),
 c/o Linköpings universitet, Department of Computer and Information Science,
 SE-58183 Linköping, Sweden.

 All rights reserved.

 THIS PROGRAM IS PROVIDED UNDER THE TERMS OF THE BSD NEW LICENSE OR THE
 GPL VERSION 3 LICENSE OR THE OSMC PUBLIC LICENSE (OSMC-PL) VERSION 1.2.
 ANY USE, REPRODUCTION OR DISTRIBUTION OF THIS PROGRAM CONSTITUTES
 RECIPIENT'S ACCEPTANCE OF THE OSMC PUBLIC LICENSE OR THE GPL VERSION 3,
 ACCORDING TO RECIPIENTS CHOICE.

 The OpenModelica software and the OSMC (Open Source Modelica Consortium)
 Public License (OSMC-PL) are obtained from OSMC, either from the above
 address, from the URLs: http://www.openmodelica.org or
 http://www.ida.liu.se/projects/OpenModelica, and in the OpenModelica
 distribution. GNU version 3 is obtained from:
 http://www.gnu.org/copyleft/gpl.html. The New BSD License is obtained from:
 http://www.opensource.org/licenses/BSD-3-Clause.

 This program is distributed WITHOUT ANY WARRANTY; without even the implied
 warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE, EXCEPT AS
 EXPRESSLY SET FORTH IN THE BY RECIPIENT SELECTED SUBSIDIARY LICENSE
 CONDITIONS OF OSMC-PL.
"""

import shutil
import abc
import getpass
import logging
import json
import os
import pathlib
import psutil
import signal
import subprocess
import sys
import tempfile
import time
import uuid
import pyparsing
import zmq
import warnings

# TODO: replace this with the new parser
from OMPython.OMTypedParser import parseString as om_parser_typed
from OMPython.OMParser import om_parser_basic


# define logger using the current module name as ID
logger = logging.getLogger(__name__)


class DummyPopen():
    def __init__(self, pid):
        self.pid = pid
        self.process = psutil.Process(pid)
        self.returncode = 0

    def poll(self):
        return None if self.process.is_running() else True

    def kill(self):
        return os.kill(self.pid, signal.SIGKILL)

    def wait(self, timeout):
        return self.process.wait(timeout=timeout)


class OMCSessionException(Exception):
    pass


class OMCSessionBase(metaclass=abc.ABCMeta):

    def __init__(self, readonly=False):
        self._readonly = readonly
        self._omc_cache = {}

    def execute(self, command):
        warnings.warn("This function is depreciated and will be removed in future versions; "
                      "please use sendExpression() instead", DeprecationWarning, stacklevel=1)

        return self.sendExpression(command, parsed=False)

    @abc.abstractmethod
    def sendExpression(self, command, parsed=True):
        """
        Sends an expression to the OpenModelica. The return type is parsed as if the
        expression was part of the typed OpenModelica API (see ModelicaBuiltin.mo).
        * Integer and Real are returned as Python numbers
        * Strings, enumerations, and typenames are returned as Python strings
        * Arrays, tuples, and MetaModelica lists are returned as tuples
        * Records are returned as dicts (the name of the record is lost)
        * Booleans are returned as True or False
        * NONE() is returned as None
        * SOME(value) is returned as value
        """
        pass

    def ask(self, question, opt=None, parsed=True):
        p = (question, opt, parsed)

        if self._readonly and question != 'getErrorString':
            # can use cache if readonly
            if p in self._omc_cache:
                return self._omc_cache[p]

        if opt:
            expression = f'{question}({opt})'
        else:
            expression = question

        logger.debug('OMC ask: %s  - parsed: %s', expression, parsed)

        try:
            res = self.sendExpression(expression, parsed=parsed)
        except OMCSessionException:
            logger.error("OMC failed: %s, %s, parsed=%s", question, opt, parsed)
            raise

        # save response
        self._omc_cache[p] = res

        return res

    # TODO: Open Modelica Compiler API functions. Would be nice to generate these.
    def loadFile(self, filename):
        return self.ask('loadFile', f'"{filename}"')

    def loadModel(self, className):
        return self.ask('loadModel', className)

    def isModel(self, className):
        return self.ask('isModel', className)

    def isPackage(self, className):
        return self.ask('isPackage', className)

    def isPrimitive(self, className):
        return self.ask('isPrimitive', className)

    def isConnector(self, className):
        return self.ask('isConnector', className)

    def isRecord(self, className):
        return self.ask('isRecord', className)

    def isBlock(self, className):
        return self.ask('isBlock', className)

    def isType(self, className):
        return self.ask('isType', className)

    def isFunction(self, className):
        return self.ask('isFunction', className)

    def isClass(self, className):
        return self.ask('isClass', className)

    def isParameter(self, className):
        return self.ask('isParameter', className)

    def isConstant(self, className):
        return self.ask('isConstant', className)

    def isProtected(self, className):
        return self.ask('isProtected', className)

    def getPackages(self, className="AllLoadedClasses"):
        return self.ask('getPackages', className)

    def getClassRestriction(self, className):
        return self.ask('getClassRestriction', className)

    def getDerivedClassModifierNames(self, className):
        return self.ask('getDerivedClassModifierNames', className)

    def getDerivedClassModifierValue(self, className, modifierName):
        return self.ask('getDerivedClassModifierValue', f'{className}, {modifierName}')

    def typeNameStrings(self, className):
        return self.ask('typeNameStrings', className)

    def getComponents(self, className):
        return self.ask('getComponents', className)

    def getClassComment(self, className):
        try:
            return self.ask('getClassComment', className)
        except pyparsing.ParseException as ex:
            logger.warning("Method 'getClassComment' failed for %s", className)
            logger.warning('OMTypedParser error: %s', ex.msg)
            return 'No description available'

    def getNthComponent(self, className, comp_id):
        """ returns with (type, name, description) """
        return self.ask('getNthComponent', f'{className}, {comp_id}')

    def getNthComponentAnnotation(self, className, comp_id):
        return self.ask('getNthComponentAnnotation', f'{className}, {comp_id}')

    def getImportCount(self, className):
        return self.ask('getImportCount', className)

    def getNthImport(self, className, importNumber):
        # [Path, id, kind]
        return self.ask('getNthImport', f'{className}, {importNumber}')

    def getInheritanceCount(self, className):
        return self.ask('getInheritanceCount', className)

    def getNthInheritedClass(self, className, inheritanceDepth):
        return self.ask('getNthInheritedClass', f'{className}, {inheritanceDepth}')

    def getParameterNames(self, className):
        try:
            return self.ask('getParameterNames', className)
        except KeyError as ex:
            logger.warning('OMPython error: %s', ex)
            # FIXME: OMC returns with a different structure for empty parameter set
            return []

    def getParameterValue(self, className, parameterName):
        try:
            return self.ask('getParameterValue', f'{className}, {parameterName}')
        except pyparsing.ParseException as ex:
            logger.warning('OMTypedParser error: %s', ex.msg)
            return ""

    def getComponentModifierNames(self, className, componentName):
        return self.ask('getComponentModifierNames', f'{className}, {componentName}')

    def getComponentModifierValue(self, className, componentName):
        return self.ask(question='getComponentModifierValue', opt=f'{className}, {componentName}')

    def getExtendsModifierNames(self, className, componentName):
        return self.ask('getExtendsModifierNames', f'{className}, {componentName}')

    def getExtendsModifierValue(self, className, extendsName, modifierName):
        return self.ask(question='getExtendsModifierValue', opt=f'{className}, {extendsName}, {modifierName}')

    def getNthComponentModification(self, className, comp_id):
        # FIXME: OMPython exception Results KeyError exception

        # get {$Code(....)} field
        # \{\$Code\((\S*\s*)*\)\}
        value = self.ask('getNthComponentModification', f'{className}, {comp_id}', parsed=False)
        value = value.replace("{$Code(", "")
        return value[:-3]
        # return self.re_Code.findall(value)

    # function getClassNames
    #   input TypeName class_ = $Code(AllLoadedClasses);
    #   input Boolean recursive = false;
    #   input Boolean qualified = false;
    #   input Boolean sort = false;
    #   input Boolean builtin = false "List also builtin classes if true";
    #   input Boolean showProtected = false "List also protected classes if true";
    #   output TypeName classNames[:];
    # end getClassNames;
    def getClassNames(self, className=None, recursive=False, qualified=False, sort=False, builtin=False,
                      showProtected=False):
        value = self.ask(
            'getClassNames',
            (f'{className}, ' if className else '') +
            f'recursive={str(recursive).lower()}, '
            f'qualified={str(qualified).lower()}, '
            f'sort={str(sort).lower()}, '
            f'builtin={str(builtin).lower()}, '
            f'showProtected={str(showProtected).lower()}'
        )
        return value


class OMCSessionZMQ(OMCSessionBase):

    def __init__(self, readonly=False, timeout=10.00,
                 docker=None, dockerContainer=None, dockerExtraArgs=None, dockerOpenModelicaPath="omc",
                 dockerNetwork=None, port=None, omhome: str = None):
        if dockerExtraArgs is None:
            dockerExtraArgs = []

        super().__init__(readonly=readonly)

        self.omhome = self._get_omhome(omhome=omhome)

        self._omc_process = None
        self._omc_command = None
        self._omc = None
        self._dockerCid = None
        self._serverIPAddress = "127.0.0.1"
        self._interactivePort = None
        # FIXME: this code is not well written... need to be refactored
        self._temp_dir = pathlib.Path(tempfile.gettempdir())
        # generate a random string for this session
        self._random_string = uuid.uuid4().hex
        # omc log file
        self._omc_log_file = None
        try:
            self._currentUser = getpass.getuser()
            if not self._currentUser:
                self._currentUser = "nobody"
        except KeyError:
            # We are running as a uid not existing in the password database... Pretend we are nobody
            self._currentUser = "nobody"

        # Locating and using the IOR
        if sys.platform != 'win32' or docker or dockerContainer:
            self._port_file = "openmodelica." + self._currentUser + ".port." + self._random_string
        else:
            self._port_file = "openmodelica.port." + self._random_string
        self._docker = docker
        self._dockerContainer = dockerContainer
        self._dockerExtraArgs = dockerExtraArgs
        self._dockerOpenModelicaPath = dockerOpenModelicaPath
        self._dockerNetwork = dockerNetwork
        self._create_omc_log_file("port")
        self._timeout = timeout
        self._port_file = ((pathlib.Path("/tmp") if docker else self._temp_dir) / self._port_file).as_posix()
        self._interactivePort = port
        # set omc executable path and args
        self._set_omc_command([
                               "--interactive=zmq",
                               "--locale=C",
                               f"-z={self._random_string}"
                               ])
        # start up omc executable, which is waiting for the ZMQ connection
        self._start_omc_process(timeout)
        # connect to the running omc instance using ZMQ
        self._connect_to_omc(timeout)

    def __del__(self):
        try:
            self.sendExpression("quit()")
        except OMCSessionException:
            pass
        self._omc_log_file.close()
        try:
            self._omc_process.wait(timeout=2.0)
        except subprocess.TimeoutExpired:
            if self._omc_process:
                logger.warning("OMC did not exit after being sent the quit() command; "
                               "killing the process with pid=%s", self._omc_process.pid)
                self._omc_process.kill()
                self._omc_process.wait()

    def _create_omc_log_file(self, suffix):
        if sys.platform == 'win32':
            log_filename = f"openmodelica.{suffix}.{self._random_string}.log"
        else:
            log_filename = f"openmodelica.{self._currentUser}.{suffix}.{self._random_string}.log"
        # this file must be closed in the destructor
        self._omc_log_file = open(self._temp_dir / log_filename, "w+")

    def _start_omc_process(self, timeout):
        if sys.platform == 'win32':
            omhome_bin = (self.omhome / "bin").as_posix()
            my_env = os.environ.copy()
            my_env["PATH"] = omhome_bin + os.pathsep + my_env["PATH"]
            self._omc_process = subprocess.Popen(self._omc_command, stdout=self._omc_log_file,
                                                 stderr=self._omc_log_file, env=my_env)
        else:
            # set the user environment variable so omc running from wsgi has the same user as OMPython
            my_env = os.environ.copy()
            my_env["USER"] = self._currentUser
            self._omc_process = subprocess.Popen(self._omc_command, stdout=self._omc_log_file,
                                                 stderr=self._omc_log_file, env=my_env)
        if self._docker:
            for i in range(0, 40):
                try:
                    with open(self._dockerCidFile, "r") as fin:
                        self._dockerCid = fin.read().strip()
                except IOError:
                    pass
                if self._dockerCid:
                    break
                time.sleep(timeout / 40.0)
            try:
                os.remove(self._dockerCidFile)
            except FileNotFoundError:
                pass
            if self._dockerCid is None:
                logger.error("Docker did not start. Log-file says:\n%s" % (open(self._omc_log_file.name).read()))
                raise OMCSessionException("Docker did not start (timeout=%f might be too short especially if you did "
                                          "not docker pull the image before this command)." % timeout)

        dockerTop = None
        if self._docker or self._dockerContainer:
            if self._dockerNetwork == "separate":
                self._serverIPAddress = json.loads(subprocess.check_output(["docker", "inspect", self._dockerCid]).decode().strip())[0]["NetworkSettings"]["IPAddress"]
            for i in range(0, 40):
                if sys.platform == 'win32':
                    break
                dockerTop = subprocess.check_output(["docker", "top", self._dockerCid]).decode().strip()
                self._omc_process = None
                for line in dockerTop.split("\n"):
                    columns = line.split()
                    if self._random_string in line:
                        try:
                            self._omc_process = DummyPopen(int(columns[1]))
                        except psutil.NoSuchProcess:
                            raise OMCSessionException(
                                f"Could not find PID {dockerTop} - is this a docker instance spawned "
                                f"without --pid=host?\nLog-file says:\n{open(self._omc_log_file.name).read()}")
                        break
                if self._omc_process is not None:
                    break
                time.sleep(timeout / 40.0)
            if self._omc_process is None:
                raise OMCSessionException("Docker top did not contain omc process %s:\n%s\nLog-file says:\n%s"
                                          % (self._random_string, dockerTop, open(self._omc_log_file.name).read()))
        return self._omc_process

    def _getuid(self):
        """
        The uid to give to docker.
        On Windows, volumes are mapped with all files are chmod ugo+rwx,
        so uid does not matter as long as it is not the root user.
        """
        return 1000 if sys.platform == 'win32' else os.getuid()

    def _set_omc_command(self, omc_path_and_args_list):
        """Define the command that will be called by the subprocess module.

        On Windows, use the list input style of the subprocess module to
        avoid problems resulting from spaces in the path string.
        Linux, however, only works with the string version.
        """
        if (self._docker or self._dockerContainer) and sys.platform == "win32":
            extraFlags = ["-d=zmqDangerousAcceptConnectionsFromAnywhere"]
            if not self._interactivePort:
                raise OMCSessionException("docker on Windows requires knowing which port to connect to. For "
                                          "dockerContainer=..., the container needs to have already manually exposed "
                                          "this port when it was started (-p 127.0.0.1:n:n) or you get an error later.")
        else:
            extraFlags = []
        if self._docker:
            if sys.platform == "win32":
                p = int(self._interactivePort)
                dockerNetworkStr = ["-p", "127.0.0.1:%d:%d" % (p, p)]
            elif self._dockerNetwork == "host" or self._dockerNetwork is None:
                dockerNetworkStr = ["--network=host"]
            elif self._dockerNetwork == "separate":
                dockerNetworkStr = []
                extraFlags = ["-d=zmqDangerousAcceptConnectionsFromAnywhere"]
            else:
                raise OMCSessionException('dockerNetwork was set to %s, but only \"host\" or \"separate\" is allowed')
            self._dockerCidFile = self._omc_log_file.name + ".docker.cid"
            omcCommand = ["docker", "run", "--cidfile", self._dockerCidFile, "--rm", "--env", "USER=%s" % self._currentUser, "--user", str(self._getuid())] + self._dockerExtraArgs + dockerNetworkStr + [self._docker, self._dockerOpenModelicaPath]
        elif self._dockerContainer:
            omcCommand = ["docker", "exec", "--env", "USER=%s" % self._currentUser, "--user", str(self._getuid())] + self._dockerExtraArgs + [self._dockerContainer, self._dockerOpenModelicaPath]
            self._dockerCid = self._dockerContainer
        else:
            omcCommand = [str(self._get_omc_path())]
        if self._interactivePort:
            extraFlags = extraFlags + ["--interactivePort=%d" % int(self._interactivePort)]

        self._omc_command = omcCommand + omc_path_and_args_list + extraFlags

        return self._omc_command

    def _get_omhome(self, omhome: str = None):
        # use the provided path
        if omhome is not None:
            return pathlib.Path(omhome)

        # check the environment variable
        omhome = os.environ.get('OPENMODELICAHOME')
        if omhome is not None:
            return pathlib.Path(omhome)

        # Get the path to the OMC executable, if not installed this will be None
        path_to_omc = shutil.which("omc")
        if path_to_omc is not None:
            return pathlib.Path(path_to_omc).parents[1]

        raise OMCSessionException("Cannot find OpenModelica executable, please install from openmodelica.org")

    def _get_omc_path(self) -> pathlib.Path:
        return self.omhome / "bin" / "omc"

    def _connect_to_omc(self, timeout):
        self._omc_zeromq_uri = "file:///" + self._port_file
        # See if the omc server is running
        attempts = 0
        self._port = None
        while True:
            if self._dockerCid:
                try:
                    self._port = subprocess.check_output(["docker", "exec", self._dockerCid, "cat", self._port_file],
                                                         stderr=subprocess.DEVNULL).decode().strip()
                    break
                except subprocess.CalledProcessError:
                    pass
            else:
                if os.path.isfile(self._port_file):
                    # Read the port file
                    with open(self._port_file, 'r') as f_p:
                        self._port = f_p.readline()
                    os.remove(self._port_file)
                    break

            attempts += 1
            if attempts == 80.0:
                name = self._omc_log_file.name
                self._omc_log_file.close()
                logger.error("OMC Server did not start. Please start it! Log-file says:\n%s" % open(name).read())
                raise OMCSessionException(f"OMC Server did not start (timeout={timeout}). "
                                          "Could not open file {self._port_file}")
            time.sleep(timeout / 80.0)

        self._port = self._port.replace("0.0.0.0", self._serverIPAddress)
        logger.info(f"OMC Server is up and running at {self._omc_zeromq_uri} pid={self._omc_process.pid} cid={self._dockerCid}")

        # Create the ZeroMQ socket and connect to OMC server
        context = zmq.Context.instance()
        self._omc = context.socket(zmq.REQ)
        self._omc.setsockopt(zmq.LINGER, 0)  # Dismisses pending messages if closed
        self._omc.setsockopt(zmq.IMMEDIATE, True)  # Queue messages only to completed connections
        self._omc.connect(self._port)

    def sendExpression(self, command, parsed=True):
        p = self._omc_process.poll()  # check if process is running
        if p is not None:
            raise OMCSessionException("Process Exited, No connection with OMC. Create a new instance of OMCSessionZMQ!")

        attempts = 0
        while True:
            try:
                self._omc.send_string(str(command), flags=zmq.NOBLOCK)
                break
            except zmq.error.Again:
                pass
            attempts += 1
            if attempts >= 50:
                self._omc_log_file.seek(0)
                log = self._omc_log_file.read()
                self._omc_log_file.close()
                raise OMCSessionException(f"No connection with OMC (timeout={self._timeout}). Log-file says: \n{log}")
            time.sleep(self._timeout / 50.0)
        if command == "quit()":
            self._omc.close()
            self._omc = None
            return None
        else:
            result = self._omc.recv_string()
            if parsed is True:
                try:
                    return om_parser_typed(result)
                except pyparsing.ParseException as ex:
                    logger.warning('OMTypedParser error: %s. Returning the basic parser result.', ex.msg)
                    try:
                        return om_parser_basic(result)
                    except (TypeError, UnboundLocalError) as ex:
                        logger.warning('OMParser error: %s. Returning the unparsed result.', ex)
                        return result
            else:
                return result
