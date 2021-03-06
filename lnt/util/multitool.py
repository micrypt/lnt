import os
import sys

class MultiTool(object):
    """
    This object defines a generic command line tool instance, which dynamically
    builds its commands from a module dictionary.

    Example usage::

      import multitool

      def action_foo(name, args):
          "the foo command"

          ... 

      tool = multitool.MultiTool(locals())
      if __name__ == '__main__':
        tool.main(sys.argv)

    Any function beginning with "action_" is considered a tool command. It's
    name is defined by the function name suffix. Underscores in the function
    name are converted to '-' in the command line syntax. Actions ending ith
    "-debug" are not listed in the help.
    """

    def __init__(self, locals):
        # Create the list of commands.
        self.commands = dict((name[7:].replace('_','-'), f)
                             for name,f in locals.items()
                             if name.startswith('action_'))

    def usage(self, name):
        print >>sys.stderr, "Usage: %s <command> [options] ... arguments ..." %(
            os.path.basename(name),)
        print >>sys.stderr
        print >>sys.stderr, """\
Use ``%s <command> --help`` for more information on a specific command.\n""" % (
            os.path.basename(name),)
        print >>sys.stderr, "Available commands:"
        cmds_width = max(map(len, self.commands))
        for name,func in sorted(self.commands.items()):
            if name.endswith("-debug"):
                continue

            print >>sys.stderr, "  %-*s - %s" % (cmds_width, name, func.__doc__)
        sys.exit(1)

    def main(self, args=None):
        if args is None:
            args = sys.argv

        if len(args) < 2 or args[1] not in self.commands:
            if len(args) >= 2:
                print >>sys.stderr,"error: invalid command %r\n" % args[1]
            self.usage(args[0])

        cmd = args[1]
        self.commands[cmd]('%s %s' % (os.path.basename(args[0]), cmd), args[2:])
