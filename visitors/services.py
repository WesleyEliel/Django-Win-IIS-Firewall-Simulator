import subprocess


def is_super_admin(user):
    return user.is_authenticated and user.is_superuser


def block_ip_in_firewall(ip_address):
    try:
        # Create a new firewall rule to block the IP
        command = [
            'netsh', 'advfirewall', 'firewall', 'add', 'rule',
            'name=BlockIP_{}'.format(ip_address),
            'dir=in',
            'action=block',
            'remoteip={}'.format(ip_address),
            'protocol=any',
            'enable=yes'
        ]
        subprocess.run(command, check=True, shell=True)
        return True, ""
    except subprocess.CalledProcessError as exc:
        print(exc)
        return False, exc.__str__()


def unblock_ip_in_firewall(ip_address):
    try:
        # Delete the firewall rule
        command = [
            'netsh', 'advfirewall', 'firewall', 'delete', 'rule',
            'name=BlockIP_{}'.format(ip_address)
        ]
        subprocess.run(command, check=True, shell=True)
        return True, ""
    except subprocess.CalledProcessError as exc:
        print(exc)
        return False, exc.__str__()
