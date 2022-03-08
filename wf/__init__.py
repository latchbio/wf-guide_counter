"""
Latch wrapper of Fulcrom Genomics' Guide-Counter.
"""

import subprocess
from pathlib import Path

from latch import small_task, workflow
from latch.types import LatchFile


@small_task
def guide_counter_task(
    reads: LatchFile,
    output_name: str,
) -> (LatchFile, LatchFile, LatchFile):

    _guide_counter_cmd = [
        "guide-counter",
        "count",
        "--input",
        str(Path(reads).resolve()),
        "--library",
        "/root/brunello.csv",
        "--output",
        output_name,
    ]

    counts = Path(f"/root/{output_name}.counts.txt")
    extended_counts = Path(f"/root/{output_name}.extended-counts.txt")
    stats = Path(f"/root/{output_name}.stats.txt")

    subprocess.run(_guide_counter_cmd)

    return (
        LatchFile(str(counts), f"latch:///{counts}"),
        LatchFile(str(extended_counts), f"latch:///{extended_counts}"),
        LatchFile(str(stats), f"latch:///{stats}"),
    )


@workflow
def guide_counter_wf(
    reads: LatchFile,
    output_name: str,
) -> (LatchFile, LatchFile, LatchFile):
    """A better, faster way to count guides in CRISPR screens.

    Guide-Counter
    ----

    `guide-counter` is a tool for processing FASTQ files from CRISPR screen
    experiments to generate a matrix of per-sample guide counts. It can be used as
    a faster, more accurate, drop in replacement for mageck count. By default
    `guide-counter` will look for guide seqeunces in the reads with 0 or 1 mismatches
    vs. the expected guides, but can be run in exact matching mode.


    __metadata__:
        display_name: Assemble and Sort FastQ Files
        author:
            name: Fulcrum Genomics
            email:
            github:
        repository: https://github.com/fulcrumgenomics/guide-counter
        license:
            id: MIT

    Args:

        reads:
          A FastQ File (zipped or unzipped) with NGS reads from which counts
          are desired.

          __metadata__:
            display_name: Reads File

        output_name:
          The name of the output files.

          __metadata__:
            display_name:
    """
    return guide_counter_task(reads=reads, output_name=output_name)
