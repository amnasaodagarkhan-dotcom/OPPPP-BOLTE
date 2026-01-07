import subprocess

def is_admin(user_id, admin_ids):
    return user_id in admin_ids

def run_cmd(node, command):
    ssh = f"ssh {node['ssh_user']}@{node['host']} -p {node['ssh_port']} '{command}'"
    try:
        return subprocess.getoutput(ssh)
    except Exception as e:
        return str(e)
