#!/usr/bin/env python3
# EESync - easy backup / sync tool

from os import chdir, path
chdir(path.dirname(path.realpath(__file__)))
from Src.EESync import EESync # noqa


def main():
    EESync().start()


if __name__ == '__main__':
    main()
