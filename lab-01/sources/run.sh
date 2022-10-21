level_1_output="../output/level_1"
level_2_output="../output/level_2"
level_3_output="../output/level_3"
level_4_output="../output/level_4"

if [[ ! -d  "../output" ]]
then 
    if [[ ! -L "../output" ]]
    then
        mkdir "../output"
    fi
fi


if [[ ! -d  "$level_1_output" ]]
then 
    if [[ ! -L "$level_1_output" ]]
    then
        mkdir "$level_1_output"
    fi
fi

if [[ ! -d  "$level_2_output" ]]
then 
    if [[ ! -L "$level_2_output" ]]
    then
        mkdir "$level_2_output"
    fi
fi

if [[ ! -d  "$level_3_output" ]]
then 
    if [[ ! -L "$level_3_output" ]]
    then
        mkdir "$level_3_output"
    fi
fi

if [[ ! -d  "$level_4_output" ]]
then 
    if [[ ! -L "$level_4_output" ]]
    then
        mkdir "$level_4_output"
    fi
fi

runner=""

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
    $runner -m pip install --upgrade pip
    $runner -m pip install -r ./env-requirements.txt
fi

exit 0

$runner main.py -a BFS -i ../input-samples/normal/bfs.txt -o ../output/level_1/bfs_lv1.mp4 -m NORMAL \ # lv 1 bfs
| $runner main.py -a DFS -i ../input-samples/normal/dfs.txt -o ../output/level_1/dfs_lv1.mp4 -m NORMAL \ # lv 1 dfs
| $runner main.py -a UCS -i ../input-samples/normal/ucs.txt -o ../output/level_1/ucs_lv1.mp4 -m NORMAL \ # lv 1 ucs
| $runner main.py -a GBFS -i ../input-samples/normal/gbfs.txt -o ../output/level_1/gbfs_lv1.mp4 -m NORMAL \ # lv 1 gbfs
| $runner main.py -a A_STAR -i ../input-samples/normal/a_star.txt -o ../output/level_1/a_star_lv1.mp4 -m NORMAL \ # lv 1 a*
| $runner main.py -a A_STAR -i ../input-samples/bonus/1.txt -o ../output/level_2/lv2_map_1_a_star.mp4 -m BONUS \ # lv 2 map 1
| $runner main.py -a A_STAR -i ../input-samples/bonus/2.txt -o ../output/level_2/lv2_map_2_a_star.mp4 -m BONUS \ # lv 2 map 2
| $runner main.py -a A_STAR -i ../input-samples/bonus/3.txt -o ../output/level_2/lv2_map_3_a_star.mp4 -m BONUS \ # lv 2 map 3
| $runner main.py -a A_STAR -i ../input-samples/inter/1.txt -o ../output/level_3/lv3_map_1_a_star.mp4 -m INTERMEDIATE \ # lv 3 map 1
| $runner main.py -a A_STAR -i ../input-samples/inter/2.txt -o ../output/level_3/lv3_map_2_a_star.mp4 -m INTERMEDIATE \ # lv 3 map 2
| $runner main.py -a A_STAR -i ../input-samples/inter/3.txt -o ../output/level_3/lv3_map_3_a_star.mp4 -m INTERMEDIATE \ # lv 3 map 3
| $runner main.py -a A_STAR -i ../input-samples/tele/1.txt -o ../output/level_4/lv4_map_1_a_star.mp4 -m TELEPORT \ # lv 4 map 1 _ a*
| $runner main.py -a A_STAR -i ../input-samples/tele/2.txt -o ../output/level_4/lv4_map_2_a_star.mp4 -m TELEPORT \ # lv 4 map 2 _ a*
| $runner main.py -a A_STAR -i ../input-samples/tele/3.txt -o ../output/level_4/lv4_map_3_a_star.mp4 -m TELEPORT \ # lv 4 map 3 _ a*
| $runner main.py -a GBFS -i ../input-samples/tele/1.txt -o ../output/level_4/lv4_map_1_gbfs.mp4 -m TELEPORT \ # lv 4 map 1 _ gbfs
| $runner main.py -a GBFS -i ../input-samples/tele/2.txt -o ../output/level_4/lv4_map_2_gbfs.mp4 -m TELEPORT \ # lv 4 map 2 _ gbfs
| $runner main.py -a GBFS -i ../input-samples/tele/3.txt -o ../output/level_4/lv4_map_3_gbfs.mp4 -m TELEPORT \ # lv 4 map 3 _ gbfs