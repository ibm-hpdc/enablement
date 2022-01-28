#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""A simple connection script to the IBM Hyper Protect Data Controller
"""

from getpass import getpass

import argparse
import warnings

warnings.filterwarnings('ignore')
from impala.dbapi import connect


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--host", dest="input_host", required=True, help="Host to connect to."
    )
    ap.add_argument(
        "-u",
        "--user",
        dest="input_user",
        required=True,
        help="User to authenticate with.",
    )
    ap.add_argument(
        "-p",
        "--password",
        dest="input_password",
        required=False,
        help="Password to authenticate with.",
    )
    ap.add_argument(
        "-q",
        "--query",
        dest="input_query",
        required=True,
        help="Query to execute.",
    )
    args = ap.parse_args()

    input_password = args.input_password
    if input_password is None:
        input_password = getpass()

    # establish connection
    con = connect(
        host=args.input_host,
        port=10010,
        user=args.input_user,
        password=input_password,
        use_ssl=False,
        auth_mechanism="PLAIN",
    )
    cur = con.cursor()

    # execute query and print results
    cur.execute(args.input_query)
    rows = cur.fetchall()
    print(rows)

    # cleanup
    cur.close()
    con.close()

