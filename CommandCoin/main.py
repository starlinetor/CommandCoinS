import argparse

#create top level parser
parser = argparse.ArgumentParser(
    prog='CommandCoin',
    description='Personal finance tracker'
    )

#basic debug argument to check entered arguments
parser.add_argument('-pa', '--print_arguments', help = 'prints all entered arguemnts')

#init subparser
subparser = parser.add_subparsers(help="")

parser_test = subparser.add_parser('test')
parser_setup = subparser.add_parser('setup')

arguments = parser._get_args()
sub_arguments = subparser._get_args()

print("arguments : " + str(arguments))
print("sub_arguments : " + str(sub_arguments))