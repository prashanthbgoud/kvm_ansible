import atexit
from pyVim.connect import SmartConnectNoSSL, Disconnect
from pyVmomi import vim
from tools import cli
from datetime import datetime, timedelta

def setup_args():

    """
    Get standard connection arguments
    """
    parser = cli.build_arg_parser()
    my_args = parser.parse_args()

    return cli.prompt_for_password(my_args)

def main():

    args = setup_args()
    si = None
    try:
        si = SmartConnectNoSSL(host=args.host,
                               user=args.user,
                               pwd=args.password,
                               port=int(args.port))
        atexit.register(Disconnect, si)
    except vim.fault.InvalidLogin:
        raise SystemExit("Unable to connect to host "
                         "with supplied credentials.")

    content = si.RetrieveContent()
    for child in content.rootFolder.childEntity:
        if hasattr(child, 'vmFolder'):
            datacenter = child
            vmfolder = datacenter.vmFolder
            vmlist = vmfolder.childEntity
            diff_24hour = datetime.now() - timedelta(hours = 24)
            for vm in vmlist:
                # Assuming content.rootFolder.childEntity.vmlist[..].creationTime is VM created time
                if datetime.strptime(vm.creation.Date, '%b %d %Y %I:%M%p') < diff_24hour:
                    print("VM Name: " + vm.name + "Creation Date: " + str(vm.creation.Date))

# Start program
if __name__ == "__main__":
    main()
