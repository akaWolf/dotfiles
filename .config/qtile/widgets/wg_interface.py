import subprocess

from widgets.wg_config import wg_config


def is_active():
    out = subprocess.getoutput(wg_config.active_cmd)
    return len(out) != 0


def get_statistics():
    rx = subprocess.getoutput(wg_config.rx_cmd)
    tx = subprocess.getoutput(wg_config.tx_cmd)
    return (int(rx), int(tx))
