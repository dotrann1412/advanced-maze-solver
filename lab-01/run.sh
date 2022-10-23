#!/bin/bash

input_root_dir="./input"

# check input folder
echo Checking input...
if [ -d $input_root_dir ];
then
    if [ ! -r $input_root_dir ];
    then
        chmod +r $input_root_dir --recursive
    fi
else
    echo Input folder is missing. Make sure you are running this script 'in' the right context.
    exit 1
fi

runner=""

# preparing output folder
echo Preparing output folder...
output_dir="./output"
if [ ! -d $output_dir ];
then
    mkdir $output_dir
fi

if [ ! -w $output_dir ];
then
    chmod +w $output_dir --recursive
fi

which python3 | grep -q "python3"
code_1=$?
python3 --version | grep -q "Python 3.*"
code_2=$?

# check for python version and update or install all the requirements
if [ $code_1 -eq $code_2 ] && [ $code_1 -eq 0 ]
then
    runner=$(which python3)
else
    which python3 | grep -q "python3"
    code_1=$?
    python3 --version | grep -q "Python 3.*"
    code_2=$?

    if [ $code_1 -eq $code_2 ] && [ $code_1 -eq 0 ]
    then
        runner=$(which python)
    else
        echo We didn\'t find any compatiple version of python on your machine! Install python3 first and try again.
        exit 1
    fi
fi

python_version=$($runner --version)
echo Using $python_version from $runner

pip_version=$($runner -m pip --version)

level_1_inputpath="./input/level_1"
level_2_inputpath="./input/level_2"
level_3_inputpath="./input/level_3"
advance_inputpath="./input/advance"

source_root_dir="./source"

# check the existance of source folder 
if [ -d $source_root_dir ];
then
    if [[ $? != 0 ]]
    then
        echo If any problem occurs during demo 'time' try to install pip by this command: "apt install python3-pip" \(Run with administrator permission 'if' needed\)!
    else
        echo Upgrading pip...
        $runner -m pip install --upgrade pip > /dev/null 
        echo Installing requirements...
        $runner -m pip install -r $source_root_dir/env-requirements.txt > /dev/null 
    fi
else
    echo Error! Source file not found. Let\'s check.
    exit 1
fi

set -e

# run level 1 with fully algos
if [ -d $level_1_inputpath ];   
then
    echo Running Level 1 'for' with 5 algorithms.
    $runner $source_root_dir/main.py -a BFS -m NORMAL -i $level_1_inputpath -o $output_dir
    $runner $source_root_dir/main.py -a DFS -m NORMAL -i $level_1_inputpath -o $output_dir
    $runner $source_root_dir/main.py -a UCS -m NORMAL -i $level_1_inputpath -o $output_dir

    $runner $source_root_dir/main.py -a A_STAR -m NORMAL -i $level_1_inputpath -o $output_dir -hf 1
    $runner $source_root_dir/main.py -a GBFS -m NORMAL -i $level_1_inputpath -o $output_dir -hf 1

    $runner $source_root_dir/main.py -a A_STAR -m NORMAL -i $level_1_inputpath -o $output_dir -hf 2
    $runner $source_root_dir/main.py -a GBFS -m NORMAL -i $level_1_inputpath -o $output_dir -hf 2
else
    echo Warning! Level 1 input folder is missing: $level_1_inputpath
fi

# run level 2 with A*
if [ -d $level_2_inputpath ];
then
    echo Running Level 2 with A* algorithm.
    $runner $source_root_dir/main.py -a A_STAR -m BONUS -i $level_2_inputpath -o $output_dir
else
    echo Warning! Level 2 input folder is missing: $level_2_inputpath
fi

# run level 3 with A*
if [ -d $level_3_inputpath ];
then
    echo Running Level 3 with A* algorithm.
    $runner $source_root_dir/main.py -a A_STAR -m INTERMEDIATE -i $level_3_inputpath -o $output_dir
else
    echo Warning! Level 3 input folder is missing: $level_3_inputpath
fi


# run advance level with A* and BFS
if [ -d $advance_inputpath ];
then
    echo Running advance level with A* algorithm.
    $runner $source_root_dir/main.py -a A_STAR -m TELEPORT -i $advance_inputpath -o $output_dir

    echo Running advance level with BFS algorithm.
    $runner $source_root_dir/main.py -a BFS -m TELEPORT -i $advance_inputpath -o $output_dir
else
    echo Warning! Advance input folder is missing: $advance_inputpath
fi

echo All 'Done'! Let\'s check $output_dir.