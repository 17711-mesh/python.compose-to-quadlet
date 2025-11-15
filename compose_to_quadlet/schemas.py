from pydantic import BaseModel, Field
from typing import Dict, List, Optional

class ComposeServiceResourcesLimits(BaseModel):
    cpus: Optional[str] = None
    memory: Optional[str] = None

class ComposeServiceResourcesReservations(BaseModel):
    cpus: Optional[str] = None
    memory: Optional[str] = None

class ComposeServiceResources(BaseModel):
    limits: Optional[ComposeServiceResourcesLimits] = None
    reservations: Optional[ComposeServiceResourcesReservations] = None

class ComposeServiceDeploy(BaseModel):
    replicas: Optional[int] = Field(default=1, ge=1)
    resources: Optional[ComposeServiceResources] = None

class ComposeService(BaseModel):
    name: str
    image: str
    command: Optional[str] = None
    environment: Dict[str,str] = {}
    networks: List[str] = []
    volumes: List[str] = []
    ports: List[str] = []
    depends_on: List[str] = []
    restart: Optional[str] = None
    deploy: Optional[ComposeServiceDeploy] = None

class ComposeNetwork(BaseModel):
    name: str
    driver: Optional[str] = None
    ipam_subnet: Optional[str] = None
    ipam_gateway: Optional[str] = None

class ComposeVolume(BaseModel):
    name: str
    driver: Optional[str] = None

class ComposeFile(BaseModel):
    services: Dict[str, ComposeService] = {}
    networks: Dict[str, ComposeNetwork] = {}
    volumes: Dict[str, ComposeVolume] = {}

    @classmethod
    def from_raw(cls, raw: dict):
        services={}
        for name,svc in raw.get("services",{}).items():
            services[name]=ComposeService(name=name, **svc)
        networks={}
        for name,net in raw.get("networks",{}).items():
            networks[name]=ComposeNetwork(name=name, **net)
        volumes={}
        for name,vol in raw.get("volumes",{}).items():
            volumes[name]=ComposeVolume(name=name, **vol)
        return cls(services=services, networks=networks, volumes=volumes)
