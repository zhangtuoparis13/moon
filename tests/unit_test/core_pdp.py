"""
unit test for moon/core/pdp
"""

import argparse
from moon.core.pdp.core import get_intra_extensions


REQUESTS = {
    'authz': [
        {
            'subject': 'user1',
            'object': 'vm1',
            'action': 'read'
        },
        {
            'subject': 'user1',
            'object': 'vm2',
            'action': 'read'
        },
        {
            'subject': 'user1',
            'object': 'vm3',
            'action': 'write'
        }
    ],
    'admin': [
        {
            'subject': 'user1',
            'object': 'subjects',
            'action': 'read'
        },
        {
            'subject': 'user2',
            'object': 'subjects',
            'action': 'write'
        }
    ]
}


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
                for i in range(len(REQUESTS['authz'])):
                    sub = REQUESTS['authz'][i]['subject']
                    obj = REQUESTS['authz'][i]['object']
                    act = REQUESTS['authz'][i]['action']
                    result = intra_extensions.get_installed_intra_extensions()[ixk].authz(sub, obj, act)
                    print('xxxxxxxx test authz: ', result)

                for i in range(len(REQUESTS['admin'])):
                    sub = REQUESTS['admin'][i]['subject']
                    obj = REQUESTS['admin'][i]['object']
                    act = REQUESTS['admin'][i]['action']
                    result = intra_extensions.get_installed_intra_extensions()[ixk].admin(sub, obj, act)
                    print('yyyyyyyy test admin: ', result)

                intra_extensions.get_installed_intra_extensions()[ixk].sync()

        elif args.intra_extension == 'authz':
            print ('authz option is: '+args.intra_extension)
        elif args.intra_extension == 'admin':
            pass
        elif args.intra_extension == 'intra':
            pass

        print('testing core/pdp/intra_extension.py/'+args.intra_extension+' function succeed')

    if args.inter_extension:
        pass
