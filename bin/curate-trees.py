#!/usr/bin/env python

import sys
import argparse
from pathlib import Path
import dendropy
from warnings import warn


def parseArgs():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="Curate phylogenetic trees (i.e., their specification files).",
    )

    parser.add_argument(
        "--treeFiles",
        nargs="+",
        help="The tree files to curate.",
    )

    parser.add_argument(
        "--outSuffix",
        default=".treefile-curated",
        help="The suffix to use on curated output files.",
    )

    parser.add_argument(
        "--dryRun",
        action="store_true",
        help="Just print what would be done.",
    )

    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite pre-existing result files.",
    )

    parser.add_argument(
        "--rootNode",
        help="Re-root the tree on the incoming branch to the tip node with this name.",
    )

    parser.add_argument(
        "--collapse",
        type=float,
        help=(
            "A floating-point support value. Branches with support less than this "
            "value will be collapsed (to form polytomies)."
        ),
    )

    parser.add_argument(
        "--ladderize",
        choices=("ascending", "descending"),
        help="How to (optionally) ladderize the tree after re-rooting.",
    )

    parser.add_argument(
        "--format",
        default="newick",
        choices=("fasta", "phylip", "newick", "nexml", "nexus"),
        help="The output format.",
    )

    parser.add_argument(
        "--scale",
        default=1.0,
        type=float,
        help=(
            "Factor to scale the length of the branches leading to the descendants "
            "of the new root (if --rootNode is used). This can be used to reduce "
            "the length of very long branches that result from rerooting on a distant "
            "outgroup. If you use this option for an image in a publication, you of "
            "course must point out that you have done so!"
        ),
    )

    return parser.parse_args()


def main():
    args = parseArgs()

    if not (args.rootNode or args.ladderize):
        exit(
            "Nothing to do - exiting. Use one or both of --rootNode (for re-rooting) "
            "or --ladderize if you want me to do something!"
        )

    for treefile in map(Path, args.treeFiles):
        curated = treefile.parent / f"{treefile.stem}{args.outSuffix}"
        if curated.exists() and not args.force:
            print(
                f"Output {str(curated)!r} exists. Skipping. Use --force to overwrite.",
                file=sys.stderr,
            )
            continue

        with open(treefile) as fp:
            tree = dendropy.Tree.get(
                file=fp, schema="newick", preserve_underscores=True
            )

        # Nodes must either have a taxon (for tips) or a 'label' (interpreted as the
        # support value on the incoming branch of internal nodes).
        for node in tree.preorder_node_iter():
            if node.label and node.taxon:
                # It's sufficiently weird to find a label on a tip branch that we should
                # wonder a) whether the code that created the support values was sane,
                # and b) whether these labels are in fact support values. If the value
                # is 100.0 there's no harm in ignoring it, but we issue a warning. If
                # we've been given a tree with branch labels that are numeric but not
                # support values, a taxon node with a label on it is a pretty good sign
                # that something is amiss.
                msg = (
                    f"Node {node!r} has a label and a taxon. It should have one or "
                    "the other, not both. The label is supposed to be a support "
                    "value, and tips (taxa) normally won't have one because they "
                    "always have 100% support."
                )
                if float(node.label) == 100.0:
                    warn(msg)
                else:
                    exit(msg)

        if args.collapse is not None:
            for node in tree.postorder_node_iter():
                if (
                    node.is_internal()
                    and node.label is not None
                    and float(node.label) < args.collapse
                ):
                    # Collapse this node so its children become children of this
                    # node's parent.
                    node.edge.collapse()

        # Re-root.
        if args.rootNode:
            node = tree.find_node_with_taxon_label(args.rootNode)
            assert node is not None
            tree.reroot_at_edge(
                node.edge,
                update_bipartitions=True,
                length1=node.edge.length / args.scale,
                length2=node.edge.length / args.scale,
            )

        if args.ladderize:
            # The reorder function is from dendropy v5.0.2 (released Sept 2024).
            tree.reorder()
            tree.ladderize(args.ladderize == "ascending")

        if args.dryRun:
            print(f"Would write curated tree file {str(curated)!r}.")
        else:
            tree.write(path=curated, schema=args.format)
            print(f"Wrote curated tree file {str(curated)!r}.")


if __name__ == "__main__":
    main()
