import sys
import argparse
import timeit
import datetime

from .version import __version__
from .common import (
    get_logger,
    get_file_list,
    read_file_list,
)

from .bam2gt import bam2gt
from .bam2gt2 import bam2gt2
from .gt2pt import gt2pt
from .bam2vcf import bam2vcf
from .bam2vcf2 import bam2vcf2
from .bam2gdf import bam2gdf
from .gt2html import gt2html
from .bam2html import bam2html
from .fq2bam import fq2bam
from .bam2bam import bam2bam
from .bam2sdf import bam2sdf
from .sdf2gdf import sdf2gdf
from .pgkb import pgkb
from .minivcf import minivcf
from .merge import merge
from .summary import summary
from .meta import meta
from .compare import compare
from .cpa import cpa
from .plotcov import plotcov
from .check import check
from .liftover import liftover
from .peek import peek
from .snp import snp
from .compare2 import compare2

def _get_bam_list(bc, bd, bl):
    """Get the list of BAM files.

    Returns:
        list[str]: List of BAM files.

    Args:
        bc (list[str]): List of BAM files from the console.
        bd (str): Path to directory containing BAM files.
        bl (str): Path to file containing BAM filenames.
    """
    if bc:
        result = bc
    elif bd:
        result = get_file_list(bd, ".bam")
    elif bl:
        result = read_file_list(bl)
    else:
        raise ValueError("BAM files not provided")
    return result

def get_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--version",
        action="version",
        version=f"PyPGx v{__version__}",
        help="print the PyPGx version number and exit"
    )

    subparsers = parser.add_subparsers(
        dest="tool",
        metavar="tool",
        help="name of the tool",
    )

    bam2gt_parser = subparsers.add_parser(
        "bam2gt",
        help="convert BAM files to a genotype file",
    )
    bam2gt_parser.add_argument(
        "snp_caller",
        help="SNP caller ('gatk' or 'bcftools')"
    )
    bam2gt_parser.add_argument(
        "fasta_file",
        help="reference FASTA file"
    )
    bam2gt_parser.add_argument(
        "target_gene",
        help="name of target gene (e.g. 'cyp2d6')"
    )
    bam2gt_parser.add_argument(
        "genome_build",
        help="genome build ('hg19' or 'hg38')"
    )
    bam2gt_parser.add_argument(
        "data_type",
        help="type of sequencing data ('wgs' or 'ts')",
    )
    bam2gt_parser.add_argument(
        "proj_dir",
        help="output files will be written to this directory",
    )
    bam2gt_parser.add_argument(
        "bam_file",
        nargs="*",
        help="input BAM files"
    )
    bam2gt_parser.add_argument(
        "--bam_dir",
        metavar="DIR",
        help="use all BAM files in this directory as input"
    )
    bam2gt_parser.add_argument(
        "--bam_list",
        metavar="FILE",
        help="list of input BAM files, one file per line"
    )
    bam2gt_parser.add_argument(
        "--control_gene",
        metavar="STR",
        help="name or region of control gene (e.g. ‘vdr’, "
            + "‘chr12:48232319-48301814’)"
    )
    bam2gt_parser.add_argument(
        "--dbsnp_file",
        metavar="FILE",
        help="dbSNP VCF file, used by GATK to add rs numbers"
    )
    bam2gt_parser.add_argument(
        "--temp_dir",
        metavar="DIR",
        help="temporary files will be written to this directory"
    )

    bam2gt2_parser = subparsers.add_parser(
        "bam2gt2",
        help="convert BAM files to genotype files [SGE]",
    )
    bam2gt2_parser.add_argument(
        "conf_file",
        help="configuration file",
    )

    gt2pt_parser = subparsers.add_parser(
        "gt2pt",
        help="convert a genotype file to phenotypes",
    )
    gt2pt_parser.add_argument(
        "gt",
        help="genotype file",
    )
    gt2pt_parser.add_argument(
        "-o",
        metavar="FILE",
        help="output to FILE [stdout]",
    )

    bam2vcf_parser = subparsers.add_parser(
        "bam2vcf",
        help="convert BAM files to a VCF file"
    )
    bam2vcf_parser.add_argument(
        "snp_caller",
        help="SNP caller ('gatk' or 'bcftools')"
    )
    bam2vcf_parser.add_argument(
        "fasta_file",
        help="reference FASTA file"
    )
    bam2vcf_parser.add_argument(
        "target_gene",
        help="name or region of target gene (e.g. ‘cyp2d6’, "
            + "‘chr22:42512500-42551883’)"
    )
    bam2vcf_parser.add_argument(
        "output_file",
        help="write output to this file"
    )
    bam2vcf_parser.add_argument(
        "genome_build",
        help="genome build ('hg19' or 'hg38')"
    )
    bam2vcf_parser.add_argument(
        "bam_file",
        nargs="*",
        help="input BAM files"
    )
    bam2vcf_parser.add_argument(
        "--bam_dir",
        metavar="DIR",
        help="use all BAM files in this directory as input"
    )
    bam2vcf_parser.add_argument(
        "--bam_list",
        metavar="FILE",
        help="list of input BAM files, one file per line"
    )
    bam2vcf_parser.add_argument(
        "--dbsnp_file",
        metavar="FILE",
        help="dbSNP VCF file, used by GATK to add rs numbers"
    )
    bam2vcf_parser.add_argument(
        "--java_options",
        metavar="STR",
        help="Java-specific arguments for GATK (e.g. '-Xmx4G')"
    )
    bam2vcf_parser.add_argument(
        "--temp_dir",
        metavar="DIR",
        help="temporary files will be written to this directory"
    )

    bam2vcf2_parser = subparsers.add_parser(
        "bam2vcf2",
        help="convert BAM files to a VCF file [SGE]",
    )
    bam2vcf2_parser.add_argument(
        "conf_file",
        help="configuration file",
    )

    bam2gdf_parser = subparsers.add_parser(
        "bam2gdf",
        help="convert BAM files to a GDF file",
    )
    bam2gdf_parser.add_argument(
        "genome_build",
        help="genome build ('hg19' or 'hg38')",
    )
    bam2gdf_parser.add_argument(
        "target_gene",
        help="name of target gene (e.g. 'cyp2d6')",
    )
    bam2gdf_parser.add_argument(
        "control_gene",
        help="name or region of control gene (e.g. ‘vdr’, "
            + "‘chr12:48232319-48301814’)"
    )
    bam2gdf_parser.add_argument(
        "output_file",
        help="write output to this file"
    )
    bam2gdf_parser.add_argument(
        "bam_file",
        nargs="*",
        help="input BAM files"
    )
    bam2gdf_parser.add_argument(
        "--bam_dir",
        metavar="DIR",
        help="use all BAM files in this directory as input"
    )
    bam2gdf_parser.add_argument(
        "--bam_list",
        metavar="FILE",
        help="list of input BAM files, one file per line"
    )

    gt2html_parser = subparsers.add_parser(
        "gt2html",
        help="convert a genotype file to an HTML report",
    )
    gt2html_parser.add_argument(
        "gt",
        help="genotype file",
    )
    gt2html_parser.add_argument(
        "-o",
        metavar="FILE",
        help="output to FILE [stdout]",
    )

    bam2html_parser = subparsers.add_parser(
        "bam2html",
        help="convert a BAM file to an HTML report [SGE]",
    )
    bam2html_parser.add_argument(
        "conf",
        help="configuration file",
    )

    fq2bam_parser = subparsers.add_parser(
        "fq2bam",
        help="convert FASTQ files to BAM files [SGE]",
    )
    fq2bam_parser.add_argument(
        "conf",
        help="configuration file",
    )

    bam2bam_parser = subparsers.add_parser(
        "bam2bam",
        help="realign BAM files to another reference genome [SGE]",
    )
    bam2bam_parser.add_argument(
        "conf",
        help="configuration file",
    )

    bam2sdf_parser = subparsers.add_parser(
        "bam2sdf",
        help="convert BAM files to a SDF file",
    )
    bam2sdf_parser.add_argument(
        "gb",
        help="genome build",
    )
    bam2sdf_parser.add_argument(
        "tg",
        help="target gene",
    )
    bam2sdf_parser.add_argument(
        "cg",
        help="control gene or region",
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

    sdf2gdf_parser = subparsers.add_parser(
        "sdf2gdf",
        help="convert a SDF file to a GDF file",
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
        action="store_true",
        help="extract first three guidelines for testing",
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
        help="target region",
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
        help="target region",
    )
    merge_parser.add_argument(
        "-o",
        metavar="FILE",
        help="output to FILE [stdout]",
    )

    summary_parser = subparsers.add_parser(
        "summary",
        help="create summary file using Stargazer data",
    )
    summary_parser.add_argument(
        "gt",
        help="genotype file",
    )
    summary_parser.add_argument(
        "-o",
        metavar="FILE",
        help="output to FILE [stdout]",
    )

    meta_parser = subparsers.add_parser(
        "meta",
        help="create meta file from summary files",
    )
    meta_parser.add_argument(
        "sf",
        nargs="+",
        help="summary file",
    )
    meta_parser.add_argument(
        "-o",
        metavar="FILE",
        help="output to FILE [stdout]",
    )

    compare_parser = subparsers.add_parser(
        "compare",
        help="compare genotype files",
    )
    compare_parser.add_argument(
        "gt",
        nargs="+",
        help="genotype file",
    )
    compare_parser.add_argument(
        "-o",
        metavar="FILE",
        help="output to FILE [stdout]",
    )

    cpa_parser = subparsers.add_parser(
        "cpa",
        help="run change point analysis for copy number",
    )
    cpa_parser.add_argument(
        "rdata",
        help="RData file",
    )
    cpa_parser.add_argument(
        "-o",
        metavar="FILE",
        help="output to FILE [stdout]",
    )

    plotcov_parser = subparsers.add_parser(
        "plotcov",
        help="plot coverage data to PDF file",
    )
    plotcov_parser.add_argument(
        "sdf",
        help="SDF file",
    )
    plotcov_parser.add_argument(
        "out",
        help="PDF file",
    )

    check_parser = subparsers.add_parser(
        "check",
        help="check table files for Stargazer",
    )
    check_parser.add_argument(
        "star",
        help="star allele table file",
    )
    check_parser.add_argument(
        "snp",
        help="SNP table file",
    )

    liftover_parser = subparsers.add_parser(
        "liftover",
        help="convert variants in SNP table from hg19 to hg38",
    )
    liftover_parser.add_argument(
        "star",
        help="star allele table file",
    )
    liftover_parser.add_argument(
        "snp",
        help="SNP table file",
    )
    liftover_parser.add_argument(
        "tg",
        help="target gene",
    )
    liftover_parser.add_argument(
        "-o",
        metavar="FILE",
        help="output to FILE [stdout]",
    )

    peek_parser = subparsers.add_parser(
        "peek",
        help="find all possible star alleles from VCF file",
    )
    peek_parser.add_argument(
        "vcf",
        help="VCF file",
    )
    peek_parser.add_argument(
        "-o",
        metavar="FILE",
        help="output to FILE [stdout]",
    )

    snp_parser = subparsers.add_parser(
        "snp",
        help="view variant data for sample/star allele pairs",
    )
    snp_parser.add_argument(
        "vcf",
        help="VCF file",
    )
    snp_parser.add_argument(
        "pair",
        nargs="+",
        help="sample/star allele pair",
    )
    snp_parser.add_argument(
        "-o",
        metavar="FILE",
        help="output to FILE [stdout]",
    )

    compare2_parser = subparsers.add_parser(
        "compare2",
        help="compare two genotype files",
    )
    compare2_parser.add_argument(
        "truth_file",
        help="truth genotype file",
    )
    compare2_parser.add_argument(
        "test_file",
        help="test genotype file",
    )
    compare2_parser.add_argument(
        "sample_map",
        help="tab-delimited text file for sample name mapping",
    )
    compare2_parser.add_argument(
        "-o",
        metavar="FILE",
        help="output to FILE [stdout]",
    )

    return parser

def main():
    start_time = timeit.default_timer()
    parser = get_parser()
    args = parser.parse_args()

    logger = get_logger()
    logger.info(f"PyPGx v{__version__}")
    logger.info("Command:")
    logger.info("    {}".format(" ".join(sys.argv)))

    result = ""

    if args.tool == "bam2gt":
        bam2gt(**vars(args))

    elif args.tool == "bam2gt2":
        bam2gt2(**vars(args))

    elif args.tool == "gt2pt":
        result = gt2pt(args.gt)

    elif args.tool == "bam2vcf":
        bam2vcf(**vars(args))

    elif args.tool == "bam2vcf2":
        bam2vcf2(**vars(args))

    elif args.tool == "bam2gdf":
        bam2gdf(**vars(args))

    elif args.tool == "gt2html":
        result = gt2html(args.gt)

    elif args.tool == "bam2html":
        bam2html(args.conf)

    elif args.tool == "fq2bam":
        fq2bam(args.conf)

    elif args.tool == "bam2bam":
        bam2bam(args.conf)

    elif args.tool == "bam2sdf":
        result = bam2sdf(args.gb, args.tg, args.cg, args.bam)

    elif args.tool == "sdf2gdf":
        result = sdf2gdf(args.sdf, args.id)

    elif args.tool == "pgkb":
        result = pgkb(args.t)

    elif args.tool == "minivcf":
        result = minivcf(args.vcf, args.region)

    elif args.tool == "merge":
        result = merge(args.vcf, args.r)
    
    elif args.tool == "summary":
        result = summary(args.gt)

    elif args.tool == "meta":
        result = meta(args.sf)

    elif args.tool == "compare":
        result = compare(args.gt)

    elif args.tool == "cpa":
        result = cpa(args.rdata)

    elif args.tool == "plotcov":
        plotcov(args.sdf, args.out)

    elif args.tool == "check":
        check(args.star, args.snp)

    elif args.tool == "liftover":
        result = liftover(args.star, args.snp, args.tg)

    elif args.tool == "peek":
        result = peek(args.vcf)

    elif args.tool == "snp":
        result = snp(args.vcf, args.pair)

    elif args.tool == "compare2":
        result = compare2(**vars(args))

    else:
        pass

    stop_time = timeit.default_timer()
    elapsed_time = str(
        datetime.timedelta(seconds=(stop_time - start_time))
    ).split(".")[0]

    logger.info(f"Elapsed time: {elapsed_time}")
    logger.info("PyPGx finished")

    if hasattr(args, "o") and result:
        if args.o:
            with open(args.o, "w") as f:
                f.write(result)
        else:
            sys.stdout.write(result)

if __name__ == "__main__":
    main()
