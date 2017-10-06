from argparse import ArgumentParser, Namespace
from configparser import ConfigParser
import logging
from os import getcwd, path
import sys
from traceback import print_exc
from typing import Dict, List, Sequence

from OpenSSL import crypto

from quick_csr import __version__


DEFAULT_CONFIG_LOCATION = '~/.quick-csr.cfg'
DEFAULT_PROFILE = 'default'
DEFAULT_SETTINGS = {'key_size': 4096,
                    'target_folder': getcwd()}


logger = logging.getLogger(__name__)


def parse_args(argv: List[str] = sys.argv[1:]) -> Namespace:
    parser = ArgumentParser(
        'Generates certificate signing requests (PKCS #10/PEM) with subject '
        'information that are defined in a configuration file.',
        epilog='Due to a bug in the optparse module, the meta variable for '
               'the --config option cannot yet be rendered as '
               '[PATH[:PROFILE]] above. Meaning, the declaration of a profile '
               'is optional and must be preceeded by a ":".')
    parser.add_argument(
        '-c', '--config', default=DEFAULT_CONFIG_LOCATION,
        # metavar='[PATH[:PROFILE]]',
        # bug refs: https://bugs.python.org/issue11874,
        #           https://github.com/python/cpython/pull/1826
        help='Configuration file location (default: {}) and profile (default: '
             '{}) separated by a colon.'.format(DEFAULT_CONFIG_LOCATION,
                                                DEFAULT_PROFILE)
    )
    parser.add_argument(
        '--version', action="version", version='quick-csr ' + __version__,
        help='Print version and exit.')
    parser.add_argument('commonName')
    parser.add_argument('alternativeName', nargs="*")

    args = parser.parse_args(argv)

    if ':' in args.config:
        args.config_location, args.config_profile = args.config.split(':', 1)
        if not args.config_location:
            args.config_location = DEFAULT_CONFIG_LOCATION
    else:
        args.config_location, args.config_profile = args.config, None
    delattr(args, 'config')

    return args


def parse_config(args: Namespace) -> ConfigParser:
    # for the record: the configparser module is a time swallowing pita
    location = path.expanduser(args.config_location)
    parser = ConfigParser(default_section='default')
    parser.optionxform = str  # meh
    parser.read(location)
    return parser


def generate_plan(args: Namespace, parser: ConfigParser) -> Dict[str, str]:
    result = DEFAULT_SETTINGS.copy()
    result.update(parser.defaults())
    if args.config_profile is not None:
        result.update(parser[args.config_profile])
    result['commonName'] = args.commonName
    result['alternativeNames'] = args.alternativeName
    return result


def generate_request(plan: Dict[str, str]) -> crypto.X509Req:
    request = crypto.X509Req()
    subject = request.get_subject()

    for key in ('commonName', 'countryName', 'stateOrProvinceName',
                'localityName', 'organizationName', 'organizationalUnitName'):
        setattr(subject, key, plan[key])

    if plan['alternativeNames']:
        alternativeNames = ', '.join(
            'DNS: ' + x for x in plan['alternativeNames']).encode()
        san_extension = crypto.X509Extension(b'subjectAltName', False,
                                             alternativeNames)
        request.add_extensions([san_extension])

    return request


def generate_key(size) -> crypto.PKey:
    # TODO make length configurable
    result = crypto.PKey()
    result.generate_key(crypto.TYPE_RSA, int(size))
    return result


def process(plan: Dict[str, str]) -> None:
    print('Generating Certificate Signing Request and private key with these '
          'options:\n')
    for key, value in plan.items():
        if not value:
            value = './.'
        if isinstance(value, Sequence) and not isinstance(value, str):
            value = ', '.join(value)
        print('{:<23}:  {}'.format(key, value))
    print()

    request = generate_request(plan)
    key_pair = generate_key(plan['key_size'])
    request.set_pubkey(key_pair)
    request.sign(key_pair, 'sha512')

    target_folder = path.expanduser(plan['target_folder'])
    common_path = path.join(target_folder, plan['commonName'])
    with open(common_path + '.csr.pem', 'wb') as f:
        print('Writing {}'.format(f.name))
        f.write(crypto.dump_certificate_request(crypto.FILETYPE_PEM, request))
    with open(common_path + '.key', 'wb') as f:
        print('Writing {}'.format(f.name))
        f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, key_pair))


def main() -> None:
    try:
        args = parse_args()
        parser = parse_config(args)
        plan = generate_plan(args, parser)
        process(plan)
        raise SystemExit(0)
    except SystemExit:
        raise
    except Exception:
        print('An unhandled exception occurred, please report this bug:')
        print_exc()
        raise SystemExit(3)


if __name__ == "__main__":
    main()
