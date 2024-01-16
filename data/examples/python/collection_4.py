from inline import itest

def benchmark(args):
    if args.amp:
        _logger.warning("Overriding precision to 'amp' since --amp flag set.")
        args.precision = "amp"
    _logger.info(
        f"Benchmarking in {args.precision} precision. "
        f'{"NHWC" if args.channels_last else "NCHW"} layout. '
        f'torchscript {"enabled" if args.torchscript else "disabled"}'
    )

    bench_kwargs = vars(args).copy()
    bench_kwargs.pop("amp")
    model = bench_kwargs.pop("model")
    batch_size = bench_kwargs.pop("batch_size")

    bench_fns = (InferenceBenchmarkRunner,)
    prefixes = ("infer",)
    if args.bench == "both":
        bench_fns = (InferenceBenchmarkRunner, TrainBenchmarkRunner)
        prefixes = ("infer", "train")
    elif args.bench == "train":
        bench_fns = (TrainBenchmarkRunner,)
        prefixes = ("train",)
    elif args.bench.startswith("profile"):
        # specific profiler used if included in bench mode string, otherwise default to deepspeed, fallback to fvcore
        if "deepspeed" in args.bench:
            assert (
                has_deepspeed_profiling
            ), "deepspeed must be installed to use deepspeed flop counter"
            bench_kwargs["profiler"] = "deepspeed"
        elif "fvcore" in args.bench:
            assert (
                has_fvcore_profiling
            ), "fvcore must be installed to use fvcore flop counter"
            bench_kwargs["profiler"] = "fvcore"
        bench_fns = (ProfileRunner,)
        batch_size = 1

    model_results = OrderedDict(model=model)
    for prefix, bench_fn in zip(prefixes, bench_fns):
        run_results = _try_run(
            model, bench_fn, initial_batch_size=batch_size, bench_kwargs=bench_kwargs
        )
        if prefix and "error" not in run_results:
            run_results = {"_".join([prefix, k]): v for k, v in run_results.items()}
            itest().given(prefix, "train").given(run_results, {"count": 1}).check_eq(run_results,{'train_count': 1})
        model_results.update(run_results)
    if "error" not in model_results:
        param_count = model_results.pop(
            "infer_param_count", model_results.pop("train_param_count", 0)
        )
        model_results.setdefault("param_count", param_count)
        model_results.pop("train_param_count", 0)
    return model_results
