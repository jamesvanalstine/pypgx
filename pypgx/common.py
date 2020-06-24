import argparse
import logging
import io
import pkgutil

LINE_BREAK1 = "-" * 70
LINE_BREAK2 = "*" * 70

logging.basicConfig(level=logging.INFO)

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

    return parser

def is_namespace(x):
    return isinstance(x, argparse.Namespace)

def is_file(x):
    return isinstance(x, io.IOBase)

def read_gene_table():
    result = {}
    text = pkgutil.get_data(__name__, "resources/sg/gene_table.txt").decode()
    for line in text.strip().split("\n"):
        fields = line.split("\t")
        gene = fields[1]
        if gene == "name":
            header = fields
            continue
        result[gene] = dict(zip(header, fields))
    return result

def parse_region(x):
    return (
        x.split(":")[0],
        int(x.split(":")[1].split("-")[0]),
        int(x.split(":")[1].split("-")[1]),
    )

def sort_regions(x):
    def f(x):
        r = parse_region(x)
        if "X" in r[0]:
            chr = 23
        elif "Y" in r[0]:
            chr = 24
        else:
            chr = int(r[0].replace("chr", ""))
        return (chr, r[1], r[2])
    return sorted(x, key = f)