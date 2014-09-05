import argparse
from moon.core.pdp.extension import Extension
from moon.core.pdp.intra_extension_authz import AuthzExtension
from moon.core.pdp.intra_extension_admin import AdminExtension
from moon.core.pdp.intra_extension import IntraExtension

'''
this module tests the core, intra-extention, inter-extention code
'''

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--core', action='store_true')
    parser.add_argument('--intra_extension', action='store')
    parser.add_argument('--inter_extension', action='store_true')
    args = parser.parse_args()

    if args.core:
        pass

    if args.intra_extension:
        print('testing core/pdp/intra_extension.py/'+args.intra_extension+' function starting ...')

        if args.intra_extension == 'extension':
            pass
        elif args.intra_extension == 'authz':
            pass
        elif args.intra_extension == 'admin':
            pass
        elif args.intra_extension == 'intra':
            pass

        print('testing core/pdp/intra_extension.py/'+args.intra_extension+' function succeed')

    if args.inter_extension:
        pass