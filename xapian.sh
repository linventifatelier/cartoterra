#!/bin/bash
export MYENV=~/earthbuilding-env/lib/python2.7
export LOCALPYTHON=/usr/lib/python2.7
ln -s $LOCALPYTHON/dist-packages/xapian/__init__.py $MYENV/site-packages/xapian.py
ln -s $LOCALPYTHON/dist-packages/xapian/_xapian.so $MYENV/site-packages/
if [ ! -f $MYENV/site-packages/haystack/backends/xapian_backend.py ]
then
    ln -s $MYENV/site-packages/xapian_backend.py $MYENV/site-packages/haystack/backends/
fi

