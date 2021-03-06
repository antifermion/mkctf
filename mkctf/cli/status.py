'''
file: status.py
date: 2018-03-02
author: koromodako
purpose:

'''
# =============================================================================
#  IMPORTS
# =============================================================================
import mkctf.helper.cli as cli
from mkctf.api import MKCTFAPI
from mkctf.helper.log import app_log
from mkctf.helper.formatting import HSEP, format_text, format_rcode2str
# =============================================================================
#  FUNCTIONS
# =============================================================================
async def status(api, args):
    '''Determines the status of at least one challenge
    '''
    if not args.yes and not cli.confirm('do you really want to check status?'):
        app_log.warning("operation cancelled by user.")
        return False
    err_sep = format_text(f'{HSEP[:35]} [STDERR] {HSEP[:35]}', 'red')
    out_sep = format_text(f'{HSEP[:35]} [STDOUT] {HSEP[:35]}', 'blue')
    exc_sep = format_text(f'{HSEP[:35]} [EXCEPT] {HSEP[:35]}', 'magenta')
    chall_sep = format_text(HSEP, 'blue', attrs=['bold'])
    success = True
    async for build_result in api.status(args.tags, args.slug, args.timeout):
        rcode = build_result['rcode']
        chall_desc = format_text(f"{build_result['slug']}", 'blue')
        chall_status = format_rcode2str(rcode)
        print(chall_sep)
        print(f"{chall_desc} {chall_status}")
        if rcode < 0:
            success = False
            print(exc_sep)
            print(build_result['exception'])
        elif rcode > 0:
            print(out_sep)
            print(build_result['stdout'].decode().strip())
            print(err_sep)
            print(build_result['stderr'].decode().strip())
    return success

def setup_status(subparsers):
    parser = subparsers.add_parser('status', help="check deployed challenge's status using exploit/exploit.")
    parser.add_argument('--tags', '-t', action='append', default=[], help="challenge's tags.")
    parser.add_argument('--slug', '-s', help="challenge's slug.")
    parser.add_argument('--timeout', type=int, default=MKCTFAPI.DEFAULT_TIMEOUT, help="override default timeout for subprocesses.")
    parser.set_defaults(func=status)
