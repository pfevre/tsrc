""" Entry point for tsrc foreach """

import subprocess
import sys

import tsrc.cli
import tsrc.workspace
from tsrc import ui


class CommandFailed(tsrc.Error):
    pass


class CmdRunner(tsrc.workspace.RepoActor):
    def __init__(self, workspace, cmd, cmd_as_str, shell=False):
        self.workspace = workspace
        self.cmd = cmd
        self.cmd_as_str = cmd_as_str
        self.shell = shell

    @property
    def description(self):
        return "Running `%s` on every repo" % self.cmd_as_str

    def process(self, repo):
        full_path = self.workspace.joinpath(repo.src)
        rc = subprocess.call(self.cmd, cwd=full_path, shell=self.shell)
        if rc != 0:
            raise CommandFailed()


def main(args):
    try:
        workspace = tsrc.cli.get_workspace(args)
        workspace.load_manifest()
        cmd_runner = CmdRunner(workspace, args.cmd, args.cmd_as_str, shell=args.shell)
        tsrc.executor.run_sequence(workspace.manifest.repos, cmd_runner)
    except tsrc.Error as error:
        if error.message:
            ui.fatal(error.message)
        else:
            sys.exit(1)
    ui.info("Done", ui.check)
