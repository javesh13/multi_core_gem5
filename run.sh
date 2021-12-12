menu=$'1. 401.bzip2\n2. 429.mcf\n3. 456.hmmer\n4. 458.sjeng\n5. 470.lbm\n'
echo "$menu"
echo "Choose  Benchmark: "
read x
benchmark=""
input=""
if [ $x -eq 1 ]
then
    benchmark="401.bzip2"
    input=""
elif [ $x -eq 2 ]
then
    benchmark="429.mcf"
    input=""
elif [ $x -eq 3 ]
then
    input=""
    benchmark="456.hmmer"
elif [ $x -eq 4 ]
then
    input=""
    benchmark="458.sjeng"
elif [ $x -eq 5 ]
then
    input=""
    benchmark="470.lbm"
else
    echo "Please chose between 1-5"
fi

echo $benchmark


export BM=$benchmark
export BM_INPUT=$input
export GEM5_DIR=/home/me/gem5
export OUTPUT_DIR=$GEM5_DIR/benchmarks/$BM/m5out/
export BENCHMARK=$GEM5_DIR/benchmarks/$BM/src/benchmark
export ARGUMENT=$GEM5_DIR/benchmarks/$BM/data/$BM_INPUT
export SYS_EMU_FILE=$GEM5_DIR/configs/example/my_se.py
export INST_COUNT=10000000 #10 million
export TRACE_OUTPUT=$GEM5_DIR/benchmarks/$BM/trace_files/$BM.$INST_COUNT.gz

echo $TRACE_OUTPUT

# inst count
$GEM5_DIR/build/ARM/gem5.opt --verbose  --debug-file=$TRACE_OUTPUT --debug-flags=Exec,-ExecSymbol,Cache -d $OUTPUT_DIR $SYS_EMU_FILE  -c $BENCHMARK -o  $ARGUMENT  -I $INST_COUNT --cpu-type=O3_ARM_v7a_3 --caches --l2cache --l1d_size=64kB --l1i_size=64kB --l2_size=512kB --l1d_assoc=4 --l1i_assoc=2 --l2_assoc=8 --cacheline_size=64 --mem-size=8192MB --mem-channels=1 --cpu-clock=4GHz

