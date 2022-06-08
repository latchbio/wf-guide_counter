"""
Latch wrapper of Fulcrom Genomics' Guide-Counter.
"""

import subprocess
from enum import Enum
from pathlib import Path

from flytekit import task
from flytekitplugins.pod import Pod
from kubernetes.client.models import (V1Container, V1PodSpec,
                                      V1ResourceRequirements, V1Toleration)
from latch import workflow
from latch.types import LatchFile


class LibraryType(Enum):
    brunello = "brunello"
    brie = "brie"


def _get_96_spot_pod() -> Pod:
    """[ "c6i.24xlarge", "c5.24xlarge", "c5.metal", "c5d.24xlarge", "c5d.metal" ]"""

    primary_container = V1Container(name="primary")
    resources = V1ResourceRequirements(
        requests={"cpu": "90", "memory": "170Gi"},
        limits={"cpu": "96", "memory": "192Gi"},
    )
    primary_container.resources = resources

    return Pod(
        pod_spec=V1PodSpec(
            containers=[primary_container],
            tolerations=[
                V1Toleration(effect="NoSchedule", key="ng", value="cpu-96-spot")
            ],
        ),
        primary_container_name="primary",
    )


large_spot_task = task(task_config=_get_96_spot_pod())


@large_spot_task
def guide_counter_task(
    reads: LatchFile,
    output_name: str,
    primer_seq: str,
    library_type: LibraryType = LibraryType.brunello,
) -> (LatchFile, LatchFile, LatchFile):

    _cutadapt_cmd = [
        "cutadapt",
        "-j",
        "96",
        "-g",
        str(primer_seq),
        "-o",
        "/root/output.fastq.gz",
        reads.local_path,
    ]
    subprocess.run(_cutadapt_cmd)

    _guide_counter_cmd = [
        "guide-counter",
        "count",
        "--input",
        "/root/output.fastq.gz",
        "--library",
        f"/root/{library_type.value}.csv",
        "--output",
        output_name,
    ]

    counts = Path(f"/root/{output_name}.counts.txt")
    extended_counts = Path(f"/root/{output_name}.extended-counts.txt")
    stats = Path(f"/root/{output_name}.stats.txt")

    subprocess.run(_guide_counter_cmd)

    return (
        LatchFile(str(counts), f"latch://{counts}"),
        LatchFile(str(extended_counts), f"latch://{extended_counts}"),
        LatchFile(str(stats), f"latch://{stats}"),
    )


@workflow
def guide_counter_wf(
    reads: LatchFile,
    primer_seq: str,
    library_type: LibraryType = LibraryType.brunello,
    output_name: str = "myrun",
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

        primer_seq:
          Nucleotide sequence of primers to trim from library sequencing reads.

          __metadata__:
            display_name: Primer Sequence (for trimmming)

        library_type:
          The library type to count guides against.

          __metadata__:
            display_name: Library Type

        output_name:
          The name of the output files.

          __metadata__:
            display_name: Output Name
    """
    return guide_counter_task(
        reads=reads,
        primer_seq=primer_seq,
        output_name=output_name,
        library_type=library_type,
    )
