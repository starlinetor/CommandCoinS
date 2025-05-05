import argparse

#create top level parser
parser = argparse.ArgumentParser(
    prog='CommandCoin',
    description='Personal finance tracker'
    )

#basic debug argument to check entered arguments
parser.add_argument('-pa', '--print_arguments',
                    action='store_true', 
                    help = 'prints all entered arguemnts')

#init subparser
subparser = parser.add_subparsers(help="")

parser_test = subparser.add_parser('test')
parser_setup = subparser.add_parser('setup')

arguments = parser.parse_args()

if arguments.print_arguments:
    print("arguments : " + str(arguments))