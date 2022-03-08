guide-counter hosted with the Latch SDK 
---

This is an implementation of the guide-counter NGS count generation tool with
[Latch SDK](https://docs.latch.bio).

> guide-counter is a tool for processing FASTQ files from CRISPR screen
> experiments to generate a matrix of per-sample guide counts. It can be used as a
> faster, more accurate, drop in replacement for mageck count. By default
> guide-counter will look for guide seqeunces in the reads with 0 or 1 mismatches
> vs. the expected guides, but can be run in exact matching mode.

- [Repo](https://github.com/fulcrumgenomics/guide-counter)
- [Fulcrum Genomics](https://fulcrumgenomics.com)

## Uploading your own guide-counter

The contents of this repository were modified from the boilerplate provided by
`latch init`.

You can create your own workflow by 

You can replicate the contents of this repo by installing latch and creating
some boilerplate like so:

```
$ pip install latch
$ latch init wf-guide_counter
$ cd wf-guide_counter
```

You will notice the structure of your boilerplate repository is roughly the same
as this repository. Just modify the code in the `wf/__init__.py` and the
`Dockerfile`, run `latch register` and you should be able to upload your own
version of `guide-counter`.
