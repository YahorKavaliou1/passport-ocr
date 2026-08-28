import argparse

from passport_ocr.factory import create_pipeline


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Pass image processor")
    parser.add_argument("--input", required=True, help="Path to the pass image")
    parser.add_argument("--output", required=False, help="Path to the output JSON")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    pipeline = create_pipeline()
    result = pipeline.run(args.input)

    result_json = result.model_dump_json(indent=2)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(result_json)
    else:
        print(result_json)


if __name__ == "__main__":
    main()