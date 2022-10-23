#!/bin/bash

runner=""

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
source_root_dir="./sources"

if [[ $? != 0 ]]
then
    echo If any problem occurs during demo 'time' try to install pip by this command: "apt install python3-pip" \(Run with administrator permission 'if' needed\)!
else
    echo Upgrading pip...
    $runner -m pip install --upgrade pip > /dev/null 
    echo Installing requirements...
    $runner -m pip install -r $source_root_dir/env-requirements.txt > /dev/null 
fi

set -e



echo Running Level 1 'for' with 5 algorithms.
$runner $source_root_dir/main.py -a BFS -m NORMAL -i $level_1_inputpath -o $output_dir --github-cicd true
$runner $source_root_dir/main.py -a DFS -m NORMAL -i $level_1_inputpath -o $output_dir --github-cicd true
$runner $source_root_dir/main.py -a UCS -m NORMAL -i $level_1_inputpath -o $output_dir --github-cicd true

$runner $source_root_dir/main.py -a A_STAR -m NORMAL -i $level_1_inputpath -o $output_dir --github-cicd true -hf 1
$runner $source_root_dir/main.py -a GBFS -m NORMAL -i $level_1_inputpath -o $output_dir --github-cicd true -hf 1

$runner $source_root_dir/main.py -a A_STAR -m NORMAL -i $level_1_inputpath -o $output_dir --github-cicd true -hf 2
$runner $source_root_dir/main.py -a GBFS -m NORMAL -i $level_1_inputpath -o $output_dir --github-cicd true -hf 2

echo Running Level 2 with A* algorithm.
$runner $source_root_dir/main.py -a A_STAR -m BONUS -i $level_2_inputpath -o $output_dir --github-cicd true

echo Running Level 3 with A* algorithm.
$runner $source_root_dir/main.py -a A_STAR -m INTERMEDIATE -i $level_3_inputpath -o $output_dir --github-cicd true

echo Running advance level with A* algorithm.
$runner $source_root_dir/main.py -a A_STAR -m TELEPORT -i $advance_inputpath -o $output_dir --github-cicd true

echo Running advance level with BFS algorithm.
$runner $source_root_dir/main.py -a BFS -m TELEPORT -i $advance_inputpath -o $output_dir --github-cicd true

echo All 'Done'! Let\'s check $output_dir.