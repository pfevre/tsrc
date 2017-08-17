""" Entry point for `tsrc init` """

import os
import sys

import path

from tsrc import ui
import tsrc.workspace


def main(args):
    workspace_path = args.workspace_path or os.getcwd()
    workspace = tsrc.workspace.Workspace(path.Path(workspace_path))
    ui.info_1("Creating new workspace in", ui.bold, workspace_path)
    try:
        workspace.init_manifest(args.manifest_url, branch=args.branch)
        workspace.load_manifest()
        workspace.clone_missing()
        workspace.set_remotes()
        workspace.copy_files()
    except tsrc.Error as error:
        if error.message:
            ui.fatal(error)
        else:
            sys.exit(1)
    ui.info("Done", ui.check)
