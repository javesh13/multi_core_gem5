# -- an example to run SPEC 429.mcf on gem5, put it under 429.mcf folder --
export BM=401.bzip2
export BM_INPUT=input.program
export GEM5_DIR=/home/me/gem5
export OUTPUT_DIR=$GEM5_DIR/benchmarks/$BM/m5out/
export BENCHMARK=$GEM5_DIR/benchmarks/$BM/src/benchmark
export BENCHMARK2=$GEM5_DIR/benchmarks/hello_arm/benchmark_hello
export ARGUMENT=$GEM5_DIR/benchmarks/$BM/data/$BM_INPUT
export SYS_EMU_FILE=$GEM5_DIR/configs/example/my_se.py
export INST_COUNT=100000 #10 million
export TRACE_OUTPUT=$BM.out.gz


# # inst count
$GEM5_DIR/build/ARM/gem5.opt --verbose  --debug-file=$TRACE_OUTPUT --debug-flags=Exec,-ExecSymbol,Cache -d $OUTPUT_DIR $SYS_EMU_FILE  -c "$BENCHMARK;$BENCHMARK2" -o  "$ARGUMENT;$ARGUMENT"  -I $INST_COUNT --cpu-type=O3_ARM_v7a_3 --num-cpus=2 --caches --l2cache --l1d_size=64kB --l1i_size=64kB --l2_size=512kB --l1d_assoc=4 --l1i_assoc=2 --l2_assoc=8 --cacheline_size=64 --mem-size=8192MB --mem-channels=2 --cpu-clock=4GHz

# $GEM5_DIR/build/ARM/gem5.opt --verbose  --debug-file=$TRACE_OUTPUT --debug-flags=Exec,-ExecSymbol,Cache -d $OUTPUT_DIR $SYS_EMU_FILE  --bench="$BENCHMARK-$BENCHMARK" -I $INST_COUNT --cpu-type=O3_ARM_v7a_3 --num-cpus=2 --caches --l2cache --l1d_size=64kB --l1i_size=64kB --l2_size=512kB --l1d_assoc=4 --l1i_assoc=2 --l2_assoc=8 --cacheline_size=64 --mem-size=8192MB --mem-channels=2 --cpu-clock=4GHz
