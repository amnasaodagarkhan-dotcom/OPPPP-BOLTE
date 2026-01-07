from modules.utils import run_cmd

def create_lxc(node_name, name, ram, cpu):
    node = {"host":"127.0.0.1","ssh_user":"root","ssh_port":22}  # placeholder
    run_cmd(node, f"lxc-create -n {name} -t ubuntu")
    run_cmd(node, f"lxc-start -n {name}")
    run_cmd(node, f"lxc config set {name} limits.memory {ram}")
    run_cmd(node, f"lxc config set {name} limits.cpu {cpu}")
    return f"✅ VPS `{name}` created on `{node_name}`"

def delete_lxc(node_name, name):
    node = {"host":"127.0.0.1","ssh_user":"root","ssh_port":22}
    run_cmd(node, f"lxc-stop -n {name}")
    run_cmd(node, f"lxc-destroy -n {name}")
    return f"🗑️ VPS `{name}` deleted"

def restart_lxc(node_name, name):
    node = {"host":"127.0.0.1","ssh_user":"root","ssh_port":22}
    run_cmd(node, f"lxc-stop -n {name}")
    run_cmd(node, f"lxc-start -n {name}")
    return f"🔄 VPS `{name}` restarted"

def list_lxc(node_name):
    node = {"host":"127.0.0.1","ssh_user":"root","ssh_port":22}
    output = run_cmd(node, "lxc-ls")
    return f"📃 VPS on {node_name}:\n```{output}```"
