from argparse import ArgumentParser, Namespace
from configparser import ConfigParser
import logging
from os import getcwd, path
import sys
from traceback import print_exc
from typing import Dict, List, Sequence

from OpenSSL import crypto

from quick_csr import __version__


logger = logging.getLogger(__name__)


def parse_args(argv: List[str] = sys.argv[1:]) -> Namespace:
    parser = ArgumentParser(
        'Generates certificate signing requests (PKCS #10/PEM) with subject '
        'information that are defined in a configuration file.')
    config_default = '~/.quick-csr.cfg'
    # TODO allow specifiying a section with deviant values
    parser.add_argument(
        '-c', '--config', default=config_default,
        help='Configuration file location (default: {})'.format(config_default)
    )
    parser.add_argument(
        '--version', action="version", version='quick-csr ' + __version__,
        help='Print version and exit.')
    parser.add_argument('commonName')
    parser.add_argument('alternativeName', nargs="*")
    return parser.parse_args(argv)


def parse_config(location: str) -> ConfigParser:
    location = path.expanduser(location)
    parser = ConfigParser(default_section='default')
    parser.optionxform = str  # meh
    parser.read(location)
    return parser


def generate_plan(args: Namespace, parser: ConfigParser) -> Dict[str, str]:
    result = parser.defaults()
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


def generate_key() -> crypto.PKey:
    # TODO make length configurable
    result = crypto.PKey()
    result.generate_key(crypto.TYPE_RSA, 4096)
    return result


def process(plan: Dict[str, str]) -> None:
    print('Generating Certificate Signing Request and private key with these '
          'options:\n')
    for key, value in plan.items():
        if not value:
            value = './.'
        if isinstance(value, Sequence) and not isinstance(value, str):
            value = ', '.join(value)
        print('{:<24}: {}'.format(key, value))
    print()

    request = generate_request(plan)
    key_pair = generate_key()
    request.set_pubkey(key_pair)
    request.sign(key_pair, 'sha512')

    common_path = path.join(getcwd(), plan['commonName'])
    with open(common_path + '.csr.pem', 'wb') as f:
        print('Writing {}'.format(f.name))
        f.write(crypto.dump_certificate_request(crypto.FILETYPE_PEM, request))
    with open(common_path + '.key', 'wb') as f:
        print('Writing {}'.format(f.name))
        f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, key_pair))


def main() -> None:
    try:
        args = parse_args()
        parser = parse_config(args.config)
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
