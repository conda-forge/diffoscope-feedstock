import sys
from subprocess import call

FAIL_UNDER = 75

COV = [sys.executable, "-m", "coverage"]

TEST_ARGS = [
    *COV,
    "run",
    "-m",
    "--source=diffoscope",
    "--branch",
    "pytest",
    "tests",
    "-vv",
    "--tb=long",
    "--color=yes",
]

REPORT_ARGS = [
    *COV,
    "report",
    "--show-missing",
    "--skip-covered",
    f"--fail-under={FAIL_UNDER}",
]


def _join(by, args):
    if len(args) == 1:
        return args[0]
    return "(" + (by.join(args)) + ")"


K_SIMPLE = [
    "test_berkeley_db",
    "test_code_is_black_clean",
    "test_elf",
    "test_icc",
    "test_item_rdb",
    "test_macho",
    "test_rlib",
    "test_wasm",
    "test_docx",
]

K_COMPOUND = [
    ["test_pdf", ["test_no_differences"]],
    ["test_html", ["test_diff"]],
    # https://github.com/conda-forge/diffoscope-feedstock/pull/161
    ["test_epub", ["test_differences", "test_compare_non_existing"]],
    [
        "test_zip",
        [
            "test_compressed_files",
            "test_extra_fields",
            "test_jmod_metadata",
            "test_commented",
            "test_metadata",
            "test_mozzip_compressed_files",
            "test_mozzip_metadata",
        ],
    ],
    # https://github.com/conda-forge/diffoscope-feedstock/pull/164
    ["test_ffprobe", ["test_diff"]],
    ["test_xz", ["test_content_diff"]],
]

K_ALL = _join(
    " or ",
    [
        *K_SIMPLE,
        *[_join(" and ", [fn, _join(" or ", t)]) for fn, t in K_COMPOUND],
    ],
)

TEST_ARGS += ["-k", f"not {K_ALL}"]

if __name__ == "__main__":
    print(TEST_ARGS)
    print(REPORT_ARGS)
    sys.exit(call(TEST_ARGS) or call(REPORT_ARGS))
