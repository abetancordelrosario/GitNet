from email.policy import default
from pydoc import pager
import click
from models.draw import draw
from models.interestGraph import interestGraph
from models.dataProcessing import dataProcessing  
import cmd

class REPL(cmd.Cmd):
    def __init__(self, ctx):
        cmd.Cmd.__init__(self)
        self.ctx = ctx

    def default(self, line):
        subcommand = command.cli.commands.get(line)
        if subcommand:
            self.ctx.invoke(subcommand)
        else:
            return cmd.Cmd.default(self, line)

class command:
    
    def __init__(self):
        pass

    @click.group(invoke_without_command=True)
    @click.pass_context
    @click.option("-r", "--repository", required=True, help="Enter full name of the repository (author/repo)")
    @click.option("-t", "--token", required=True, help="Enter OAuth GitHub token")  
    def cli(ctx, repository, token):
        graph = interestGraph(repository,token)
        if ctx.invoked_subcommand is None:
            repl = REPL(ctx)
            repl.cmdloop()

    @cli.command()
    def users():
        # algorithms.get_relevant_users(self.graph)
        pass

    @cli.command()
    def b():
        """The `b` command prints a 'b'."""
        print("b")

    
    # @cli.command()    
    # def execute(self):
    #     print("hola")

