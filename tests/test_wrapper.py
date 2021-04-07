#!/usr/bin/env python3

import sys, os

from testsupport import info, run_project_executable, warn, subtest


def main() -> None:

    # Generate a small random file
    with open("rdn.txt", "w") as fp:
        fp.write(os.urandom(4096))

    # Copy the file with the system's glibc
    with subtest("Run cp with system glibc"):
        run([ "cp", "rdn.txt", "rdn.glibc.txt" ])

    # Copy files with LD_PRELOADed librw.so.1
    with subtest("Run cp with librw.so.1 preloaded"):
        run([ "cp", "rdn.txt", "rdn.librw.1.txt" ],
            extra_env={"LD_PRELOAD": "librw.so.1"})

    # Check that glibc and librw.so.1 give the same result
    with subset("Check that both resulting files are identical"):
        run([ "cmp", "rdn.glibc.txt", "rdn.librw.1.txt" ])

    # # Check that the nbytes == 0 optimisation is implemented
    # with subtest("Check that librw.so.1 avoids the syscall if nothing will be read/written"):
    #     with open("strace.log", "r+") as fp:
    #         run([ "strace", "-o", "strace.log",
    #               "cp", "rdn.txt", "rdn.librw.1.txt" ],
    #             extra_env={"LD_PRELOAD": "librw.so.1"})

if __name__ == "__main__":
    main()