# Formatter Benchmarks

This is a simple repo for benchmarking the Rome Formatter. It's a separate repo because there's no
point in bloating the tools repo with all these submodules.

Before running, please have [hyperfine](https://github.com/sharkdp/hyperfine), [rome](https://github.com/rome/tools), and [dprint](https://github.com/dprint/dprint) installed. Python 3 is required. Then run:

```
python3 bench.py
```

When running, please minimize computer usage, as other programs can affect benchmark results. Step away, have a coffee, and wait for the benchmarks to finish.

After the execution is done, you should have a `bench.md` file specific to your operating system, CPU architecture, etc.