#!/bin/bash

runner=""

output_dir="../output"
if [[ ! -d $output_dir ]]
then
    mkdir $output_dir
    chmod rw- $output_dir
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

if [[ $? != 0 ]]
then
    echo If any problem occurs during demo 'time' try to install pip by this command: "apt install python3-pip" \(Run with administrator permission 'if' needed\)!
else
    echo Upgrading pip...
    # $runner -m pip install --upgrade pip > /dev/null 
    echo Installing requirements...
    # $runner -m pip install -r ./env-requirements.txt > /dev/null 
fi

echo Running NORMAL mode 'for' 5 algorithms, ouput will be written to $output_dir. Enjoy!

$runner main.py -a BFS -m NORMAL -i ../input-samples/normal -o $output_dir
$runner main.py -a DFS -m NORMAL -i ../input-samples/normal -o $output_dir
$runner main.py -a UCS -m NORMAL -i ../input-samples/normal -o $output_dir
$runner main.py -a A_STAR -m NORMAL -i ../input-samples/normal -o $output_dir
$runner main.py -a GBFS -m NORMAL -i ../input-samples/normal -o $output_dir

$runner main.py -a A_STAR -m BONUS -i ../input-samples/bonus -o $output_dir
$runner main.py -a A_STAR -m BONUS -i ../input-samples/bonus -o $output_dir
$runner main.py -a A_STAR -m BONUS -i ../input-samples/bonus -o $output_dir

$runner main.py -a A_STAR -m INTERMEDIATE -i ../input-samples/intermediate -o $output_dir
$runner main.py -a A_STAR -m INTERMEDIATE -i ../input-samples/intermediate -o $output_dir
$runner main.py -a A_STAR -m INTERMEDIATE -i ../input-samples/intermediate -o $output_dir

$runner main.py -a A_STAR -m TELEPORT -i ../input-samples/teleport -o $output_dir
$runner main.py -a A_STAR -m TELEPORT -i ../input-samples/teleport -o $output_dir
$runner main.py -a A_STAR -m TELEPORT -i ../input-samples/teleport -o $output_dir

$runner main.py -a GBFS -m TELEPORT -i ../input-samples/teleport -o $output_dir
$runner main.py -a GBFS -m TELEPORT -i ../input-samples/teleport -o $output_dir
$runner main.py -a GBFS -m TELEPORT -i ../input-samples/teleport -o $output_dir