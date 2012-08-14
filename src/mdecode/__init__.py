
import os, _mdecode

__dir__ = os.path.abspath(os.path.dirname(__file__))

class JavaError(Exception):
    def getJavaException(self):
        return self.args[0]
    def __str__(self):
        writer = StringWriter()
        self.getJavaException().printStackTrace(PrintWriter(writer))
        return "\n".join((super(JavaError, self).__str__(), "    Java stacktrace:", str(writer)))

class InvalidArgsError(Exception):
    pass

_mdecode._set_exception_types(JavaError, InvalidArgsError)
CLASSPATH = [os.path.join(__dir__, "jmp123.jar")]
CLASSPATH = os.pathsep.join(CLASSPATH)
_mdecode.CLASSPATH = CLASSPATH
_mdecode._set_function_self(_mdecode.initVM, _mdecode)

from _mdecode import *
