from pathlib import Path

def load_env(path:Path)->dict:
    if not path or not path.exists(): return {}
    env={}
    for line in path.read_text().splitlines():
        if "=" in line:
            k,v=line.split("=",1)
            env[k.strip()]=v.strip()
    return env
