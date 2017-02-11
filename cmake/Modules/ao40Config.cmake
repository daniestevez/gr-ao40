INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_AO40 ao40)

FIND_PATH(
    AO40_INCLUDE_DIRS
    NAMES ao40/api.h
    HINTS $ENV{AO40_DIR}/include
        ${PC_AO40_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    AO40_LIBRARIES
    NAMES gnuradio-ao40
    HINTS $ENV{AO40_DIR}/lib
        ${PC_AO40_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
)

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(AO40 DEFAULT_MSG AO40_LIBRARIES AO40_INCLUDE_DIRS)
MARK_AS_ADVANCED(AO40_LIBRARIES AO40_INCLUDE_DIRS)

