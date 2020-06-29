from typing import List

import pysam

from .common import read_gene_table, logging, sort_regions, sm_tag

logger = logging.getLogger(__name__)

def bam2sdf(tg: str, cg: str, bam: List[str]):
    """
    Create SDF file from BAM file(s).
    
    Returns:
        str: Text version of SDF file.

    Args:
        tg (str): Target gene.
        cg (str): Control gene.
        bam (list[str]): BAM file(s).
    """

    genes = read_gene_table()
    targets = [k for k, v in genes.items() if v["type"] == "target"]
    controls = [k for k, v in genes.items() if v["control"] == "yes"]
    if tg not in targets:
        raise ValueError(f"'{tg}' is not among target genes: {targets}")
    if cg not in controls:
        raise ValueError(f"'{cg}' is not among control genes: {controls}")

    # Get sample and sequence names from BAM headers.
    sm = []
    sn = []
    for x in bam:
        sm.append(sm_tag(x))

        result = pysam.view("-H", x).strip().split("\n")
        for line in result:
            fields = line.split("\t")
            if "@SQ" == fields[0]:
                for field in fields:
                    if "SN:" in field:
                        y = field.replace("SN:", "")
                        if y not in sn:
                            sn.append(y)

    logger.info(f"Sample IDs: {sm}")
    logger.info(f"Contigs: {sn}")

    # Determine whether the "chr" string should be used.
    if any(["chr" in x for x in sn]):
        chr = "chr"
    else:
        chr = ""

    tr = genes[tg]["hg19_region"].replace("chr", "")
    cr = genes[cg]["hg19_region"].replace("chr", "")

    regions = sort_regions([tr, cr])

    result = ""

    for region in regions:
        temp = pysam.depth("-a", "-Q", "1", "-r", f"{chr}{region}", *bam)
        result += temp

    return result
