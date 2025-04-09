import subprocess


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
        return True
    except subprocess.CalledProcessError as exc:
        print(exc)
        return False


def unblock_ip_in_firewall(ip_address):
    try:
        # Delete the firewall rule
        command = [
            'netsh', 'advfirewall', 'firewall', 'delete', 'rule',
            'name=BlockIP_{}'.format(ip_address)
        ]
        subprocess.run(command, check=True, shell=True)
        return True
    except subprocess.CalledProcessError as exc:
        print(exc)
        return False
