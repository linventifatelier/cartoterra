#!/bin/bash
export MYENV=~/earthbuilding-env
export LOCALPYTHON=/usr/lib/python2.7
ln -s $LOCALPYTHON/dist-packages/xapian/__init__.py $MYENV/lib/python2.7/site-packages/xapian.py
ln -s $LOCALPYTHON/dist-packages/xapian/_xapian.so $MYENV/lib/python2.7/site-packages/
if [ ! -f $MYENV/lib/python2.7/site-packages/haystack/backends/xapian_backend.py ]
then
    ln -s $MYENV/lib/python2.7/site-packages/xapian_backend.py $MYENV/lib/python2.7/site-packages/haystack/backends/
fi

