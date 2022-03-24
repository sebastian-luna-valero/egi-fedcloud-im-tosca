#!/usr/bin/env python

import sys
import argparse


def create_auth_file(vo, site):
    with open(f"{vo}-{site}-auth.dat", "w") as output_file:
        with open("vo-site-auth.dat") as input_file:
            for line in input_file.readlines():
                output_file.write(line.replace("VO", vo).replace("SITE", site))


def create_tosca_file(vo, site):
    with open(f"{vo}-{site}-tosca.yaml", "w") as output_file:
        with open("vo-site-tosca.yaml") as input_file:
            for line in input_file.readlines():
                output_file.write(line.replace("VO", vo).replace("SITE", site))


def main(argv=None):
    """script main.
    parses command line options in sys.argv, unless *argv* is given.
    """

    if argv is None:
        argv = sys.argv

    # setup command line parser
    parser = argparse.ArgumentParser(
        description='Generate config files for im-client.')

    parser.add_argument(
            "--vo",
            help = "Name of the Virtual Organization (VO)",
            required = True)

    parser.add_argument(
            "--site",
            help="Name of the site in the EGI Federation",
            required = True)

    options = parser.parse_args()
    
    create_auth_file(options.vo, options.site)
    create_tosca_file(options.vo, options.site)
   

if __name__ == "__main__":
    sys.exit(main(sys.argv))
