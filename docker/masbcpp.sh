#!/bin/bash

cd /code/pkgs/masbcpp/build
LD_LIBRARY_PATH=.:$LD_LIBRARY_PATH ./compute_ma $@
