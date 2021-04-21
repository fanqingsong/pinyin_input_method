#!/bin/sh
MYDIR=$(cd `dirname $0`; pwd)
ROOTDIR=`dirname $MYDIR`
export PYTHONPATH=${PYTHONPATH}:$ROOTDIR
echo "PYTHONPATH=${PYTHONPATH}"
# Run python in the same process as the wrapper, making the wrapper transparent regarding signals (e.g. for killing the process).
exec python "$@"