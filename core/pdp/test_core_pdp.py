import argparse
from moon.core.pdp.core import get_intra_extensions

'''
this module tests the core, intra-extention, inter-extention code
'''

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--core', action='store_true')
    parser.add_argument('--intra_extension', action='store', choices=('extension', 'authz', 'admin', 'intra'))
    parser.add_argument('--inter_extension', action='store_true')
    args = parser.parse_args()

    if args.core:
        pass

    if args.intra_extension:
        print('testing core/pdp/intra_extension.py/'+args.intra_extension+' function starting ...')

        if args.intra_extension == 'extension':
            intra_extensions = get_intra_extensions()
            intra_extensions.install_intra_extension_from_json('core/pdp/extension_setting/mls001')
            for ixk in intra_extensions.get_installed_intra_extensions():
                print(intra_extensions.get_installed_intra_extensions()[ixk].authz('user1', 'vm1', 'read'))
                print(intra_extensions.get_installed_intra_extensions()[ixk].admin('user1', 'subjects', 'read'))

        elif args.intra_extension == 'authz':
            print ('authz option is: '+args.intra_extension)
        elif args.intra_extension == 'admin':
            pass
        elif args.intra_extension == 'intra':
            pass

        print('testing core/pdp/intra_extension.py/'+args.intra_extension+' function succeed')

    if args.inter_extension:
        pass
