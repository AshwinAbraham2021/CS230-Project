import os
from multiprocessing import Pool
# from time import sleep

# SEMAPHORE = Semaphore(1)

########## !!!!! MODIFY APPROPRIATELY !!!!! ##########
TRACE_FILES = ["sssp-3.trace.gz", "sssp-5.trace.gz", "sssp-10.trace.gz", "sssp-14.trace.gz"]
########## !!!!! MODIFY APPROPRIATELY !!!!! ##########

KB = 1024
MB = 1024*1024

L2_SIZES = [(256*KB/8, 8), (256*KB/32, 32), (512*KB/8, 8)]
LLC_WAY = 16
LLC_SIZES = [8*MB/LLC_WAY, 16*MB/LLC_WAY, 32*MB/LLC_WAY, 64*MB/LLC_WAY]
REPL_POLICIES = ['lru', 'lfu', 'fifo', 'random']
BRANCH_PREDICTOR = "gshare"
CACHE_TYPES = ['EXCLUSIVE', 'INCLUSIVE', 'NON-INCLUSIVE']
N_WARM = 30
N_SIM = 70
NUM_CORES = 4

CARTES_PROD = [(REPL_POLICY, L2_SIZE, LLC_SIZE, CACHE_TYPE) for REPL_POLICY in REPL_POLICIES for L2_SIZE in L2_SIZES for LLC_SIZE in LLC_SIZES for CACHE_TYPE in CACHE_TYPES]

if not os.path.isdir("results"):
    os.system("mkdir results")


def build_stuff(REPL_POLICY, L2_SIZE, LLC_SIZE, CACHE_TYPE, num):
    with open("inc/cache_sizes.h", 'w') as f:
        # sleep(1)
        print(f'Compiling #{num} {REPL_POLICY} {L2_SIZE} {LLC_SIZE} {CACHE_TYPE}')
        f.write(f"#define L2C_SET {int(L2_SIZE[0])}\n")
        f.write(f"#define L2C_WAY {int(L2_SIZE[1])}\n")
        f.write(f"#define LLC_SET NUM_CPUS*{int(LLC_SIZE)}\n")
        f.write(f"#define LLC_WAY {int(LLC_WAY)}\n")
        if CACHE_TYPE != 'NON-INCLUSIVE':
            f.write(f"#define {CACHE_TYPE}")
        f.flush()
        # print('Made the file')
        # sleep(60)
        os.system(f"./build_champsim.sh {BRANCH_PREDICTOR} no no no no {REPL_POLICY} {NUM_CORES} {REPL_POLICY} {int(L2_SIZE[0])} {int(L2_SIZE[1])} {int(LLC_SIZE)} {LLC_WAY} {BRANCH_PREDICTOR} {CACHE_TYPE}")

def run_stuff(REPL_POLICY, L2_SIZE, LLC_SIZE, CACHE_TYPE):
    # with SEMAPHORE:
    print(f'Running {REPL_POLICIES} {L2_SIZE} {LLC_SIZE}')
    # os.system(f"./run_champsim.sh {BRANCH_PREDICTOR}-no-no-no-no-{REPL_POLICY}-{NUM_CORES}core {N_WARM} {N_SIM} {TRACE_FILE}")
    os.system(f"./run_4core.sh {BRANCH_PREDICTOR}-no-no-no-no-{REPL_POLICY}-{NUM_CORES}core-{REPL_POLICY}-{int(L2_SIZE[0])}-{int(L2_SIZE[1])}-{int(LLC_SIZE)}-{LLC_WAY}-{BRANCH_PREDICTOR}-{CACHE_TYPE} {N_WARM} {N_SIM} 0 {TRACE_FILES[0]} {TRACE_FILES[1]} {TRACE_FILES[2]} {TRACE_FILES[3]} {REPL_POLICY} {int(L2_SIZE[0])} {int(L2_SIZE[1])} {int(LLC_SIZE)} {LLC_WAY} {BRANCH_PREDICTOR} {CACHE_TYPE}")
    # os.system(f"mv results_{N_SIM}M/{TRACE_FILE}-{BRANCH_PREDICTOR}-no-no-no-no-{REPL_POLICY}-{NUM_CORES}core.txt results/{TRACE_FILE}-{int(L2_SIZE[0])}-{int(L2_SIZE[1])}-{int(LLC_SIZE)}-{int(LLC_WAY)}-{BRANCH_PREDICTOR}-no-no-no-no-{REPL_POLICY}-{NUM_CORES}core.txt")
    # os.system(f"mv results_{N_SIM}M/mix0-{BRANCH_PREDICTOR}-no-no-no-no-{REPL_POLICY}-{NUM_CORES}core.txt results/mix0-{int(L2_SIZE[0])}-{int(L2_SIZE[1])}-{int(LLC_SIZE)}-{int(LLC_WAY)}-{BRANCH_PREDICTOR}-no-no-no-no-{REPL_POLICY}-{NUM_CORES}core.txt")

if __name__ == '__main__':
    # num = 1
    # for arg in CARTES_PROD:
    #     build_stuff(arg[0], arg[1], arg[2], arg[3], num)
    #     num += 1

    with Pool(len(CARTES_PROD)) as p:
        p.starmap(run_stuff, CARTES_PROD)
