# 786
# Aldy source: test_cn_real.py
#   This file is subject to the terms and conditions defined in
#   file 'LICENSE', which is part of this source code package.

# flake8: noqa

import pytest  # noqa
import re
import subprocess
import platform
import datetime

from tempfile import NamedTemporaryFile as tmpfile

from aldy.__main__ import get_version, main
from aldy.common import script_path, log
from aldy.cn import LEFT_FUSION_PENALTY
from aldy.version import __version__


YEAR = datetime.datetime.now().year
HEADER = f"""
🐿  Aldy v{__version__} (Python {platform.python_version()} on {get_version()})
   (c) 2016-2020 Aldy Authors. All rights reserved.
   Free for non-commercial/academic use only.
""".strip()


def escape_ansi(line):
    """
    Inspired by
    https://www.tutorialspoint.com/How-can-I-remove-the-ANSI-escape-sequences-from-a-string-in-python
    """  # noqa
    return re.compile(r"(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]").sub("", line)


def assert_file(monkeypatch, file, solver, expected, params=None, output=None):
    lines = []

    def log_info(*args):
        s = str.format(*args)
        lines.append(s)

    monkeypatch.setattr(log, "info", log_info)

    args = {
        **{
            "--gene": "CYP2D6",
            "--profile": "illumina",
            "--threshold": "50",
            "--gap": "0",
            "--solver": solver,
            "--fusion-penalty": f"{LEFT_FUSION_PENALTY}",
            "--max-minor-solutions": "3",
        },
        **(params or {}),
    }
    main(["genotype", file] + [i for k, v in args.items() for i in [k, v]])
    expected = expected.strip()
    lines = escape_ansi("\n".join(lines)).strip()
    assert lines == expected


EXPECTED_NA10860 = f"""
{HEADER}
Genotyping sample NA10860.bam...
Potential CYP2D6 gene structures for NA10860:
   1: 2x*1,1x*36.ALDY (confidence: 100%)
   2: 2x*1,1x*61 (confidence: 100%)
Potential major CYP2D6 star-alleles for NA10860:
   1: 1x*1, 1x*4.021, 1x*4N.ALDY (confidence: 100%)
   2: 1x*4, 1x*4N.ALDY, 1x*139 (confidence: 100%)
   3: 1x*4.021, 1x*4J, 1x*61 (confidence: 100%)
   4: 1x*4.021, 1x*4J, 1x*83.ALDY (confidence: 100%)
   5: 1x*4.021, 1x*4M, 1x*36.ALDY (confidence: 100%)
Potential CYP2D6 star-alleles for NA10860:
   1: *1 / *4.021 + *4N.ALDY (confidence=100%)
      Minor alleles: *1.018 +rs111564371 +rs113889384, *4.021 +rs28371713, *4.1013 +rs112568578 -rs28371738
   2: *1 / *4.021 + *4N.ALDY (confidence=100%)
      Minor alleles: *1.018 +rs111564371, *4.021 +rs112568578, *4.1013 +rs113889384 +rs28371713 -rs28371738
   3: *1 / *4.021 + *4N.ALDY (confidence=100%)
      Minor alleles: *1.018 +rs28371713, *4.021 +rs111564371 +rs112568578, *4.1013 +rs113889384 -rs28371738
CYP2D6 results:
  - *1 / *4.021 + *4N.ALDY
    Minor: [*1.018 +rs111564371 +rs113889384] / [*4.021 +rs28371713] + [*4.1013 +rs112568578 -rs28371738]
    Legacy notation: [*1.018 +rs111564371 +rs113889384] / [*4.021 +rs28371713] + [*4N.ALDY +rs112568578 -rs28371738]
"""


def test_NA10860(monkeypatch, solver):
    file = script_path("aldy.tests.resources/NA10860.bam")
    assert_file(monkeypatch, file, solver, EXPECTED_NA10860)

    # file = script_path("aldy.tests.resources/NA10860_hg38.bam")
    # assert_file(monkeypatch, file, solver, EXPECTED_NA10860)


EXPECTED_NA10860_GAP = f"""
{HEADER}
Genotyping sample NA10860.bam...
Potential CYP2D6 gene structures for NA10860:
   1: 2x*1,1x*36.ALDY (confidence: 100%)
   2: 2x*1,1x*61 (confidence: 100%)
   3: 2x*1,1x*5,1x*36.ALDY (confidence: 94%)
   4: 2x*1,1x*5,1x*61 (confidence: 94%)
Potential major CYP2D6 star-alleles for NA10860:
   1: 1x*1, 1x*4.021, 1x*4N.ALDY (confidence: 100%)
   2: 1x*4, 1x*4N.ALDY, 1x*139 (confidence: 100%)
   3: 1x*4.021, 1x*4J, 1x*61 (confidence: 100%)
   4: 1x*4.021, 1x*4J, 1x*83.ALDY (confidence: 100%)
   5: 1x*4.021, 1x*4M, 1x*36.ALDY (confidence: 100%)
   6: 1x*1, 1x*4.021, 1x*4N.ALDY, 1x*5 (confidence: 96%)
   7: 1x*4, 1x*4N.ALDY, 1x*5, 1x*139 (confidence: 96%)
   8: 1x*4.021, 1x*4J, 1x*5, 1x*61 (confidence: 96%)
   9: 1x*4.021, 1x*4J, 1x*5, 1x*83.ALDY (confidence: 96%)
  10: 1x*4.021, 1x*4M, 1x*5, 1x*36.ALDY (confidence: 96%)
Best CYP2D6 star-alleles for NA10860:
   1: *1 / *4.021 + *4N.ALDY (confidence=100%)
      Minor alleles: *1.001 +rs111564371 +rs112568578 +rs113889384 +rs28371713 +rs29001678, *4.021, *4.1013 -rs28371738
CYP2D6 results:
  - *1 / *4.021 + *4N.ALDY
    Minor: [*1.001 +rs111564371 +rs112568578 +rs113889384 +rs28371713 +rs29001678] / [*4.021] + [*4.1013 -rs28371738]
    Legacy notation: [*1A +rs111564371 +rs112568578 +rs113889384 +rs28371713 +rs29001678] / [*4.021] + [*4N.ALDY -rs28371738]
"""


def test_NA10860_gap(monkeypatch, solver):
    file = script_path("aldy.tests.resources/NA10860.bam")
    assert_file(monkeypatch, file, solver, EXPECTED_NA10860_GAP, {"--gap": "0.1"})


EXPECTED_HARD = f"""
{HEADER}
Genotyping sample HARD.dump...
Potential CYP2D6 gene structures for HARD:
   1: 3x*1,1x*68,1x*80 (confidence: 100%)
Potential major CYP2D6 star-alleles for HARD:
   1: 1x*2, 1x*4, 1x*39, 1x*68, 1x*80#4K (confidence: 100%)
   2: 2x*2, 1x*4, 1x*68, 1x*80#4 (confidence: 100%)
Best CYP2D6 star-alleles for HARD:
   1: *2 + *2 / *68 + *4 + *80 (confidence=100%)
      Minor alleles: *2.001, *2.001, *4.001 -rs28588594, *68.001 -rs28371699 -rs28588594, *80#4.001
CYP2D6 results:
  - *2 + *2 / *68 + *4 + *80
    Minor: [*2.001] + [*2.001] / [*68.001 -rs28371699 -rs28588594] + [*4.001 -rs28588594] + [*80#4.001]
    Legacy notation: [*2A] + [*2A] / [*68 -rs28371699 -rs28588594] + [*4A -rs28588594] + [*80#4.001]
"""


def test_hard(monkeypatch, solver):
    file = script_path("aldy.tests.resources/HARD.dump")
    assert_file(monkeypatch, file, solver, EXPECTED_HARD, {"--profile": "pgrnseq-v1"})


EXPECTED_HARD_FUSION = f"""
{HEADER}
Genotyping sample HARD.dump...
Potential CYP2D6 gene structures for HARD:
   1: 4x*1 (confidence: 100%)
Potential major CYP2D6 star-alleles for HARD:
   1: 1x*2, 1x*4, 1x*4K, 1x*39 (confidence: 100%)
   2: 2x*2, 1x*4, 1x*4C (confidence: 100%)
Best CYP2D6 star-alleles for HARD:
   1: *2 + *2 / *4 + *4C (confidence=100%)
      Minor alleles: *2.001 +rs28371738 +rs2004511 +rs2267447 +rs1080989, *2.001, *4.001 -rs28588594, *4.011
CYP2D6 results:
  - *2 + *2 / *4 + *4C
    Minor: [*2.001 +rs28371738 +rs2004511 +rs2267447 +rs1080989] + [*2.001] / [*4.001 -rs28588594] + [*4.011]
    Legacy notation: [*2A +rs28371738 +rs2004511 +rs2267447 +rs1080989] + [*2A] / [*4A -rs28588594] + [*4L]
"""


def test_hard_fusion(monkeypatch, solver):
    file = script_path("aldy.tests.resources/HARD.dump")
    assert_file(
        monkeypatch,
        file,
        solver,
        EXPECTED_HARD_FUSION,
        {"--profile": "pgrnseq-v1", "--fusion-penalty": "5"},
    )


EXPECTED_NA10860_DEBUG_TAR = """
./
./NA10860.cn.lp
./NA10860.dump
./NA10860.log
./NA10860.major0.lp
./NA10860.major1.lp
./NA10860.minor0.lp
./NA10860.minor1.lp
./NA10860.minor2.lp
./NA10860.minor3.lp
./NA10860.yml
"""


def test_NA10860_debug(monkeypatch, solver):
    file = script_path("aldy.tests.resources/NA10860.bam")
    with tmpfile(suffix=".tar.gz") as tmp:
        with tmpfile(mode="w") as out, tmpfile(mode="w") as out_log:
            out.close()
            out_log.close()
            assert_file(
                monkeypatch,
                file,
                solver,
                EXPECTED_NA10860 + "Preparing debug archive...",
                {"--debug": tmp.name[:-7], "--log": out_log.name, "--output": out.name},
            )
            with open(script_path("aldy.tests.resources/NA10860.out.expected")) as f:
                expected = f.read()
            with open(out.name) as f:
                produced = f.read()
            assert produced == expected
            # Check logs
            with open(out_log.name) as f:
                log = f.read()
            s = "    rs1058172    42523528.C>T    3267G>A    "
            s += "(cov=  21, cn= 0.9; impact=R365H)\n"
            s = "[major] status= optimal; opt= 1.48; solution= 1x*4.021, 1x*4J, 1x*61\n"
            assert s in log

        out = subprocess.check_output(f"tar tzf {tmp.name}", shell=True).decode("utf-8")
        out = "\n".join(sorted(out.strip().split("\n")))
        assert out == EXPECTED_NA10860_DEBUG_TAR.strip()


EXPECTED_NA10860_CN = f"""
{HEADER}
Genotyping sample NA10860.bam...
Potential CYP2D6 gene structures for NA10860:
   1: 2x*1 (confidence: 100%)
Potential major CYP2D6 star-alleles for NA10860:
   1: 1x*1, 1x*4.021 (confidence: 100%)
   2: 1x*4, 1x*139 (confidence: 100%)
Best CYP2D6 star-alleles for NA10860:
   1: *1 / *4.021 (confidence=100%)
      Minor alleles: *1.001 +rs28371713 +rs29001678, *4.021
CYP2D6 results:
  - *1 / *4.021
    Minor: [*1.001 +rs28371713 +rs29001678] / [*4.021]
    Legacy notation: [*1A +rs28371713 +rs29001678] / [*4.021]
"""


def test_NA10860_cn(monkeypatch, solver):
    file = script_path("aldy.tests.resources/NA10860.bam")
    assert_file(monkeypatch, file, solver, EXPECTED_NA10860_CN, {"--cn": "1,1"})


def test_NA10860_vcf(monkeypatch, solver):
    file = script_path("aldy.tests.resources/NA10860.bam")
    with tmpfile(suffix=".vcf", mode="w") as out:
        out.close()
        assert_file(monkeypatch, file, solver, EXPECTED_NA10860, {"--output": out.name})
        with open(script_path("aldy.tests.resources/NA10860.vcf.expected")) as f:
            expected = f.read()
        with open(out.name) as f:
            produced = f.read()
        assert produced == expected.replace("aldy-v2.2", f"aldy-v{__version__}")


EXPECTED_INS = f"""
{HEADER}
Genotyping sample INS.dump...
Potential CYP2D6 gene structures for INS:
   1: 2x*1 (confidence: 100%)
Potential major CYP2D6 star-alleles for INS:
   1: 1x*1, 1x*40 (confidence: 100%)
Best CYP2D6 star-alleles for INS:
   1: *1 / *40 (confidence=100%)
      Minor alleles: *1.006, *40.001
CYP2D6 results:
  - *1 / *40
    Minor: [*1.006] / [*40.001]
    Legacy notation: [*1.006] / [*40]
"""


def test_fix_insertions(monkeypatch, solver):
    file = script_path("aldy.tests.resources/INS.dump")
    assert_file(
        monkeypatch,
        file,
        solver,
        EXPECTED_INS,
        {"--profile": "pgrnseq-v3", "--max-minor-solutions": "1"},
    )


# EXPECTED_PROFILE = f"""
# {HEADER}
# Generating profile for DPYD (1:97541297-98388616)
# Generating profile for CYP2C19 (10:96444999-96615001)
# Generating profile for CYP2C9 (10:96690999-96754001)
# Generating profile for CYP2C8 (10:96795999-96830001)
# Generating profile for CYP4F2 (19:15618999-16009501)
# Generating profile for CYP2A6 (19:41347499-41400001)
# Generating profile for CYP2D6 (22:42518899-42553001)
# Generating profile for TPMT (6:18126540-18157375)
# Generating profile for CYP3A5 (7:99244999-99278001)
# Generating profile for CYP3A4 (7:99353999-99465001)
# """


# def test_profile(monkeypatch, capsys):
#     lines = []

#     def log_info(*args):
#         s = str.format(*args)
#         lines.append(s)

#     monkeypatch.setattr(log, "info", log_info)

#     main(["profile", script_path("aldy.tests.resources/NA10860.bam")])
#     lines = escape_ansi("\n".join(lines)).strip()
#     assert lines == EXPECTED_PROFILE.strip()

#     captured = capsys.readouterr()
#     with open(script_path("aldy.tests.resources/NA10860.profile")) as f:
#         expected = f.read()
#     assert captured.out == expected
