# -- an example to run SPEC 429.mcf on gem5, put it under 429.mcf folder --
export BM=hello_arm1
export BM_INPUT=input.program
export GEM5_DIR=/home/me/gem5
export OUTPUT_DIR=$GEM5_DIR/benchmarks/hello_arm1/
export BENCHMARK=$GEM5_DIR/benchmarks/$BM/benchmark
export SYS_EMU_FILE=$GEM5_DIR/configs/example/my_se.py
export INST_COUNT=10000000 #10 million
export TRACE_OUTPUT=hello_arm.out.gz


#Originnal
# $GEM5_DIR/build/ARM/gem5.opt --verbose  --debug-flags=HWPrefetch --debug-file=$TRACE_OUTPUT --debug-flags=Exec,-ExecSymbol,Cache -d $OUTPUT_DIR $SYS_EMU_FILE  -c "$BENCHMARK"  --cpu-type=O3_ARM_v7a_3 --num-cpus=2 --caches --l2cache --l1d_size=64kB --l1i_size=64kB --l2_size=512kB --l1d_assoc=4 --l1i_assoc=2 --l2_assoc=8 --cacheline_size=64 --mem-size=8192MB --mem-channels=2 --cpu-clock=4GHz --l1d-hwp-type=StridePrefetcher 


$GEM5_DIR/build/ARM/gem5.opt --verbose  --debug-flags=CacheComp --debug-file=$TRACE_OUTPUT -d $OUTPUT_DIR $SYS_EMU_FILE  -c "$BENCHMARK"  --cpu-type=O3_ARM_v7a_3 --num-cpus=2 --caches --l2cache --l1d_size=64kB --l1i_size=64kB --l2_size=512kB --l1d_assoc=4 --l1i_assoc=2 --l2_assoc=8 --cacheline_size=64 --mem-size=8192MB --mem-channels=2 --cpu-clock=4GHz --l2-hwp-type=StridePrefetcher 

# #one program

# $GEM5_DIR/build/ARM/gem5.opt --verbose  --debug-file=$TRACE_OUTPUT --debug-flags=Exec,-ExecSymbol,Cache -d $OUTPUT_DIR $SYS_EMU_FILE  -c "$BENCHMARK" -o  "$ARGUMENT"  -I $INST_COUNT --cpu-type=O3_ARM_v7a_3 --num-cpus=1 --caches --l2cache --l1d_size=64kB --l1i_size=64kB --l2_size=512kB --l1d_assoc=4 --l1i_assoc=2 --l2_assoc=8 --cacheline_size=64 --mem-size=8192MB --mem-channels=2 --cpu-clock=4GHz --l1d-hwp-type=StridePrefetcher 


# $GEM5_DIR/build/ARM/gem5.opt --verbose  --debug-file=$TRACE_OUTPUT --debug-flags=Exec,-ExecSymbol,Cache -d $OUTPUT_DIR $SYS_EMU_FILE  --bench="$BENCHMARK-$BENCHMARK" -I $INST_COUNT --cpu-type=O3_ARM_v7a_3 --num-cpus=2 --caches --l2cache --l1d_size=64kB --l1i_size=64kB --l2_size=512kB --l1d_assoc=4 --l1i_assoc=2 --l2_assoc=8 --cacheline_size=64 --mem-size=8192MB --mem-channels=2 --cpu-clock=4GHz
