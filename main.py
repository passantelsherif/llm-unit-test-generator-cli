import sys
import cli
import pipeline


def main(argv: list[str]) -> int:
    opts = cli.parse_args(argv)
    payload = cli.read_input(opts)

    try:
        result = pipeline.run_pipeline(payload, framework=opts.framework)

        if opts.out:
            with open(opts.out, "w", encoding="utf-8") as f:
                f.write(result.tests_text)
        else:
            sys.stdout.write(result.tests_text)

        return 0
    except Exception as e:
        sys.stdout.write(pipeline.render_error(e) + "\n")
        return 1

if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
