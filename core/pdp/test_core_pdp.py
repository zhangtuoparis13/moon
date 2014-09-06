import os.path
import argparse
import pkg_resources

from moon.core.pdp.extension import Metadata

'''
this module tests the core, intra-extention, inter-extention code
'''

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--core', action='store_true')
    parser.add_argument('--intra_extension', action='store',choices=('extension','authz','admin','intra'))
    parser.add_argument('--inter_extension', action='store_true')
    args = parser.parse_args()

    if args.core:
        pass

    if args.intra_extension:
        print('testing core/pdp/intra_extension.py/'+args.intra_extension+' function starting ...')

        if args.intra_extension == 'extension':
            metadatadir = pkg_resources.resource_filename("moon", "core/pdp/extension_setting")
            metadatapath = os.path.join(metadatadir, "metadata.json")
            f = open(metadatapath)
            metadata = Metadata(f)
            print(dir(metadata))
            print(metadata.meta_rules["aggregation"])

        elif args.intra_extension == 'authz':
            print ('authz option is: '+args.intra_extension)
        elif args.intra_extension == 'admin':
            pass
        elif args.intra_extension == 'intra':
            pass

        print('testing core/pdp/intra_extension.py/'+args.intra_extension+' function succeed')

    if args.inter_extension:
        pass
