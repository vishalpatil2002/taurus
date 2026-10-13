#!/bin/sh

if [ -n "$DESTDIR" ] ; then
    case $DESTDIR in
        /*) # ok
            ;;
        *)
            /bin/echo "DESTDIR argument must be absolute... "
            /bin/echo "otherwise python's distutils will bork things."
            exit 1
    esac
fi

echo_and_run() { echo "+ $@" ; "$@" ; }

echo_and_run cd "/home/vijay/taurus/big_taurus/src/ethzasl_xsens_driver"

# ensure that Python install destination exists
echo_and_run mkdir -p "$DESTDIR/home/vijay/taurus/big_taurus/install/lib/python3/dist-packages"

# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
echo_and_run /usr/bin/env \
    PYTHONPATH="/home/vijay/taurus/big_taurus/install/lib/python3/dist-packages:/home/vijay/taurus/big_taurus/build/lib/python3/dist-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/home/vijay/taurus/big_taurus/build" \
    "/usr/bin/python3" \
    "/home/vijay/taurus/big_taurus/src/ethzasl_xsens_driver/setup.py" \
    egg_info --egg-base /home/vijay/taurus/big_taurus/build/ethzasl_xsens_driver \
    build --build-base "/home/vijay/taurus/big_taurus/build/ethzasl_xsens_driver" \
    install \
    --root="${DESTDIR-/}" \
    --install-layout=deb --prefix="/home/vijay/taurus/big_taurus/install" --install-scripts="/home/vijay/taurus/big_taurus/install/bin"
