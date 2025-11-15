from dataclasses import dataclass
from typing import Dict, List, Optional
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from .schemas import ComposeFile, ComposeService
import logging

log=logging.getLogger(__name__)

@dataclass
class QuadletContainerUnit:
    unit_name:str
    service_name:str
    image:str
    command:Optional[str]
    env:Dict[str,str]
    podman_args:List[str]

@dataclass
class QuadletNetworkUnit:
    unit_name:str
    name:str
    subnet:Optional[str]
    gateway:Optional[str]

@dataclass
class QuadletVolumeUnit:
    unit_name:str
    name:str
    driver:Optional[str]

@dataclass
class QuadletStackTarget:
    unit_name:str
    stack_name:str
    container_services:List[str]

class QuadletGenerator:
    def __init__(self, template_dir:Path):
        self.env=Environment(loader=FileSystemLoader(str(template_dir)))

    def generate(self, compose:ComposeFile, output_dir:Path, stack_name:Optional[str]):
        nets=[]; vols=[]; cont=[]
        output_dir.mkdir(parents=True, exist_ok=True)

        for net in compose.networks.values():
            unit=QuadletNetworkUnit(f"{net.name}.network", net.name, net.ipam_subnet, net.ipam_gateway)
            self._render("network.j2", unit, output_dir/unit.unit_name)
            nets.append(unit)

        for vol in compose.volumes.values():
            unit=QuadletVolumeUnit(f"{vol.name}.volume", vol.name, vol.driver)
            self._render("volume.j2", unit, output_dir/unit.unit_name)
            vols.append(unit)

        for svc in compose.services.values():
            args=[]
            if svc.deploy and svc.deploy.resources:
                r=svc.deploy.resources
                if r.limits:
                    if r.limits.memory: args.append(f"--memory={r.limits.memory}")
                    if r.limits.cpus: args.append(f"--cpus={r.limits.cpus}")
            unit=QuadletContainerUnit(
                unit_name=f"{svc.name}.container",
                service_name=svc.name,
                image=svc.image,
                command=svc.command,
                env=svc.environment,
                podman_args=args
            )
            self._render("container.j2", unit, output_dir/unit.unit_name)
            cont.append(unit)

        stack=None
        if stack_name:
            services=[f"podman-{c.service_name}.service" for c in cont]
            stack=QuadletStackTarget(f"{stack_name}.target", stack_name, services)
            self._render("stack.target.j2", stack, output_dir/stack.unit_name)

        return cont, vols, nets, stack

    def _render(self, template_name:str, unit, path:Path):
        tpl=self.env.get_template(template_name)
        path.write_text(tpl.render(unit=unit), encoding="utf-8")
