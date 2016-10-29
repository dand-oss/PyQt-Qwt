import os 
import sipconfig
import optparse 
import sys

parser = optparse.OptionParser()
#parser.add_option("-f", "--file", dest="filename", help="write report to FILE", metavar="FILE")
#parser.add_option("-q", "--quiet", action="store_false", dest="verbose", default=True, help="don't print status messages to stdout")
parser.add_option("-t", "--qt-vers", dest="qtvers", help="Qt version")
    
(options, args) = parser.parse_args()

print(args)
#parser.add_option("-t", "--qt-vers" dest="

qtconf = ""
basename = "qwt"
libname = ""
qtdir = ""
sipincdir = ""
print(options.qtvers)
if options.qtvers == '5':
    import PyQt5.QtCore
    qtconf = PyQt5.QtCore.PYQT_CONFIGURATION
    libname = basename+"-qt5"
    qtdir = "/usr/include/x86_64-linux-gnu/qt5/"
    sipincdir = "/usr/share/sip/PyQt5"
else:
    print("Qt4")
    import PyQt4.QtCore
    qtconf = PyQt4.QtCore.PYQT_CONFIGURATION
    libname = basename
    qtdir = "/usr/include/qt4/"
    sipincdir = "/usr/share/sip/PyQt4"
print(sipincdir)

# The name of the SIP build file generated by SIP and used by the build
# system.
build_file = basename + ".sbf"

# Get the SIP configuration information.
config = sipconfig.Configuration()

# Run SIP to generate the code.
print(" ".join([config.sip_bin,"-c", ".", "-I",sipincdir, qtconf['sip_flags'],"-b", build_file, basename + ".sip"]))
os.system(" ".join([config.sip_bin,"-c", ".", "-I",sipincdir, qtconf['sip_flags'],"-b", build_file, basename + ".sip"]))
#os.system(" ".join([config.sip_bin,"-c", ".", "-I","/usr/share/sip/PyQt4","-t", "WS_X11" ,"-t", "Qt_4_8_6","-b", build_file, basename + ".sip"]))
#/usr/bin/sip -c . -I /usr/share/sip/PyQt5 -t -t WS_X11 -x PyQt_NoPrintRangeBug -t Qt_4_8_6 -b qwt.sbf qwt.sip

# Create the Makefile.
makefile = sipconfig.SIPModuleMakefile(config, build_file)

# Add the library we are wrapping.  The name doesn't include any platform
# specific prefixes or extensions (e.g. the "lib" prefix on UNIX, or the
# ".dll" extension on Windows).
makefile.extra_libs = [libname]

makefile.extra_cxxflags=['-g']

# Search libraries in current directory
makefile.extra_lflags= ['-L.']

if options.qtvers == '5':
    makefile.extra_include_dirs= [qtdir,qtdir+'QtCore/',qtdir+'QtGui/',qtdir+'QtWidgets/','/usr/include/qwt/']
else:
    makefile.extra_include_dirs= [qtdir,qtdir+'QtCore/',qtdir+'Qt/','/usr/include/qwt/']

print(makefile.extra_include_dirs)
# Generate the Makefile itself.
makefile.generate()
#g++ -c -g -fPIC -I/usr/include/python2.7/ -I/usr/include/qwt -I /usr/include/qt4/QtCore -I /usr/include/qt4/QtGui -I /usr/include/qt4/ arrays.cpp 