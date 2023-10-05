#!/usr/bin/env python
# import asyncio
import sys
import time
import re
from os import system
from pprint import pp

from .modules.service.argparser import ArgParser
from .modules.service.config import Config
from .modules.service.bitbucket import BitBucket

args = ArgParser.parse(args=sys.argv[1:])

if args.repository:
    config = Config()
    bb = BitBucket(config=config)
    bb.get_repos()

    repolist = []
    for repo in bb.repositories:
        if re.search(args.repository, repo):
            repolist.append(repo)
    if len(repolist) == 0:
        print("No repositories found")
    elif len(repolist) == 1:
        print(f"Repository {repolist[0]} found")
        while True:
            system('cls' if sys.platform == 'win32' else 'clear')
            bb.check(repo=repolist[0])
            time.sleep(10)
    else:
        print(f"Multiple repositories found!")
        pp(repolist)
        print("Please refine your search")
        exit(1)
elif args.username and args.password:
    Config(username=args.username, password=args.password, workspace=args.workspace, sound=args.sound)
    exit(0)
