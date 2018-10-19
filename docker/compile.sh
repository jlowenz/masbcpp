#!/bin/bash

BUILD=/code/pkgs/masbcpp/build
if [[ ! -e $BUILD ]]; then
  mkdir -p $BUILD
fi
pushd $BUILD
cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo ..
make -j
popd
