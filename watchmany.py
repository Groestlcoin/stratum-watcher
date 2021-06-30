#! /usr/bin/env python3

import argparse
import signal

from watcher import Watcher

POOLS = [
    ["stratum+tcp://grs.suprnova.cc:5544", "groestlcoin.wentaproot:x"],
    ["stratum+tcp://hub.miningpoolhub.com:20486", "groestlcoin.wentaproot:x"],
    ["stratum+tcp://groestl.mine.zergpool.com:5333", "c=GRS"],
    ["stratum+tcp://groestl.na.mine.zergpool.com:533", "c=GRS"],
    ["stratum+tcp://groestl.eu.mine.zergpool.com:533", "c=GRS"],
    ["stratum+tcp://groestl.asia.mine.zergpool.com:5333", "c=GRS"],
    ["stratum+tcp://groestl.na.mine.zpool.ca:5333", "c=GRS"],
    ["stratum+tcp://groestl.eu.mine.zpool.ca:5333", "c=GRS"],
    ["stratum+tcp://groestl.sea.mine.zpool.ca:5333", "c=GRS"],
    ["stratum+tcp://groestl.jp.mine.zpool.ca:5333", "c=GRS"],
    ["stratum+tcp://solo.phoenixmax.org:5555", "groestlcoin.wentaproot:x"],
    ["stratum+tcp://solo.phoenixmax.org:5666", "groestlcoin.wentaproot:x"],
    ["stratum+tcp://groestl.mining-dutch.nl:3514", "groestlcoin.wentaproot:x"],
    ["stratum+tcp://asia.groestl.mining-dutch.nl:3514", "groestlcoin.wentaproot:x"],
    ["stratum+tcp://americas.groestl.mining-dutch.nl:3514", "groestlcoin.wentaproot:x"],
]

parser = argparse.ArgumentParser(
    description="Run the watcher.py script for multiple hardcoded pools"
)
parser.add_argument("--debug")
parser.add_argument(
    "--rpccookiefile",
    help="Cookie file for Groestlcoin Core RPC creds",
    default="~/.groestlcoin/.cookie",
)
args = parser.parse_args()

procs = []

# Handler for SIGINT that stops all of the processes
def sigint_handler(signal, frame):
    global procs
    for p in procs:
        p.close()
        p.terminate()


# Start all watcher processes
signal.signal(signal.SIGINT, signal.SIG_IGN)
for pool in POOLS:
    proc = Watcher(pool[0], pool[1], args.rpccookiefile, name=f"Watcher {pool[0]}")
    proc.start()
    procs.append(proc)

signal.signal(signal.SIGINT, sigint_handler)

# Interrupt and wait for all of the processes to end
for p in procs:
    p.join()
