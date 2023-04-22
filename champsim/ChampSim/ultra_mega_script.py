import os

########## !!!!! MODIFY APPROPRIATELY !!!!! ##########
TRACE_FILE = "sssp-3.trace.gz"
########## !!!!! MODIFY APPROPRIATELY !!!!! ##########

KB = 1024
MB = 1024*1024

L2_SIZES = [(256*KB/8, 8), (256*KB/32, 32), (512*KB/8, 8)]
LLC_WAY = 16
LLC_SIZES = [8*MB/LLC_WAY, 16*MB/LLC_WAY, 32*MB/LLC_WAY, 64*MB/LLC_WAY]
REPL_POLICIES = ['lru', 'lfu', 'fifo', 'random']
BRANCH_PREDICTOR = "gshare"
N_WARM = 20
N_SIM = 30

if not os.path.isdir("results"):
    os.system("mkdir results")

for REPL_POLICY in REPL_POLICIES:
    for L2_SIZE in L2_SIZES:
        for LLC_SIZE in LLC_SIZES:
            with open("inc/cache_sizes.h", 'w') as f:
                f.write(f"#define L2C_SET {int(L2_SIZE[0])}\n")
                f.write(f"#define L2C_WAY {int(L2_SIZE[1])}\n")
                f.write(f"#define LLC_SET NUM_CPUS*{int(LLC_SIZE)}\n")
                f.write(f"#define LLC_WAY {int(LLC_WAY)}\n")
            os.system(f"./build_champsim.sh {BRANCH_PREDICTOR} no no no no {REPL_POLICY} 1")
            os.system(f"./run_champsim.sh {BRANCH_PREDICTOR}-no-no-no-no-{REPL_POLICY}-1core {N_WARM} {N_SIM} {TRACE_FILE}")
            os.system(f"mv results_{N_SIM}M/{TRACE_FILE}-{BRANCH_PREDICTOR}-no-no-no-no-{REPL_POLICY}-1core.txt results/{TRACE_FILE}-{int(L2_SIZE[0])}-{int(L2_SIZE[1])}-{int(LLC_SIZE)}-{int(LLC_WAY)}-{BRANCH_PREDICTOR}-no-no-no-no-{REPL_POLICY}-1core.txt")