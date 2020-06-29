import sys
import argparse

from .common import logging
from .pgkb import pgkb
from .report import report
from .sdf2gdf import sdf2gdf
from .bam2sdf import bam2sdf
from .bam2gdf import bam2gdf
from .minivcf import minivcf
from .merge import merge
from .version import __version__

logger = logging.getLogger(__name__)

def get_parser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(
        dest="tool",
        metavar="tool",
        help="name of tool",
    )
    subparsers.required = True

    pgkb_parser = subparsers.add_parser(
        "pgkb",
        help="extract CPIC guidelines using PharmGKB API",
    )
    pgkb_parser.add_argument(
        "-o",
        metavar="FILE",
        help="output to FILE [stdout]",
    )
    pgkb_parser.add_argument(
        "-t",
        action='store_true',
        help="turn on test mode (will only look first three guidelines)",
    )

    report_parser = subparsers.add_parser(
        "report",
        help="create HTML report using data from Stargazer",
    )
    report_parser.add_argument(
        "gt",
        help="Stargazer genotype file",
    )
    report_parser.add_argument(
        "-o",
        metavar="FILE",
        help="output to FILE [stdout]",
    )

    sdf2gdf_parser = subparsers.add_parser(
        "sdf2gdf",
        help="create GDF file from SDF file",
    )
    sdf2gdf_parser.add_argument(
        "sdf",
        help="SDF file",
    )
    sdf2gdf_parser.add_argument(
        "-o",
        metavar="FILE",
        help="output to FILE [stdout]",
    )
    sdf2gdf_parser.add_argument(
        "id",
        nargs="+",
        help="sample ID",
    )

    bam2sdf_parser = subparsers.add_parser(
        "bam2sdf",
        help="create SDF file from BAM file(s)",
    )
    bam2sdf_parser.add_argument(
        "tg",
        help="target gene",
    )
    bam2sdf_parser.add_argument(
        "cg",
        help="control gene",
    )
    bam2sdf_parser.add_argument(
        "bam",
        nargs="+",
        help="BAM file",
    )
    bam2sdf_parser.add_argument(
        "-o",
        metavar="FILE",
        help="output to FILE [stdout]",
    )

    bam2gdf_parser = subparsers.add_parser(
        "bam2gdf",
        help="create GDF file from BAM file(s)",
    )
    bam2gdf_parser.add_argument(
        "tg",
        help="target gene",
    )
    bam2gdf_parser.add_argument(
        "cg",
        help="control gene",
    )
    bam2gdf_parser.add_argument(
        "bam",
        nargs="+",
        help="BAM file",
    )
    bam2gdf_parser.add_argument(
        "-o",
        metavar="FILE",
        help="output to FILE [stdout]",
    )

    minivcf_parser = subparsers.add_parser(
        "minivcf",
        help="slice VCF file",
    )
    minivcf_parser.add_argument(
        "vcf",
        help="VCF file",
    )
    minivcf_parser.add_argument(
        "region",
        help="genomic region (chr:start-end)",
    )
    minivcf_parser.add_argument(
        "-o",
        metavar="FILE",
        help="output to FILE [stdout]",
    )

    merge_parser = subparsers.add_parser(
        "merge",
        help="merge VCF files",
    )
    merge_parser.add_argument(
        "vcf",
        nargs="+",
        help="VCF file",
    )
    merge_parser.add_argument(
        "-r",
        metavar="STR",
        help="genomic region (chr:start-end)",
    )
    merge_parser.add_argument(
        "-o",
        metavar="FILE",
        help="output to FILE [stdout]",
    )

    return parser

def output(fn, result):
    if fn:
        with open(fn, "w") as f:
            f.write(result)
    else:
        sys.stdout.write(result)

def main():
    logger.info(f"PyPGx v{__version__}")
    parser = get_parser()
    args = parser.parse_args()

    logger.info(f"""Command: '{" ".join(sys.argv)}'""")
    
    if args.tool == "pgkb":
        result = pgkb(args.t)
        output(args.o, result)

    elif args.tool == "report":
        result = report(args.gt)
        output(args.o, result)

    elif args.tool == "sdf2gdf":
        result = sdf2gdf(args.sdf, args.id)
        output(args.o, result)

    elif args.tool == "bam2sdf":
        result = bam2sdf(args.tg, args.cg, args.bam)
        output(args.o, result)

    elif args.tool == "bam2gdf":
        result = bam2gdf(args.tg, args.cg, args.bam)
        output(args.o, result)

    elif args.tool == "minivcf":
        result = minivcf(args.vcf, args.region)
        output(args.o, result)

    elif args.tool == "merge":
        result = merge(args.vcf, args.r)
        output(args.o, result)

if __name__ == "__main__":
    main()
