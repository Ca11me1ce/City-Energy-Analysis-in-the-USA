#!/bin/bash
echo 'Start running...';
python outlier_process.py;
python clusters.py;
python prediction.py;
echo 'End running.'