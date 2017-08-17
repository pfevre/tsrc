""" Entry point for tsrc sync """

import sys

import tsrc
from tsrc import ui
import tsrc.cli


def main(args):
    try:
        workspace = tsrc.cli.get_workspace(args)
        workspace.update_manifest()
        workspace.load_manifest()
        workspace.clone_missing()
        workspace.set_remotes()
        workspace.sync()
        workspace.copy_files()
    except tsrc.Error as error:
        if error.message:
            ui.fatal(error.message)
        else:
            sys.exit(1)
    ui.info("Done", ui.check)
