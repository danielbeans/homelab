# 🏠 Homelab
[![Docker](https://img.shields.io/badge/Docker-24.0+-blue.svg?style=flat-square&logo=docker)](https://www.docker.com/)
[![TrueNAS](https://img.shields.io/badge/Storage-TrueNAS-0095D5?style=flat-square&logo=truenas&logoColor=white)](https://www.truenas.com/)
[![Nginx Proxy Manager](https://img.shields.io/badge/Proxy-NPM-00C7B7?style=flat-square&logo=nginx&logoColor=white)](https://nginxproxymanager.com/)
[![Cloudflare](https://img.shields.io/badge/Network-Cloudflare-F38020?style=flat-square&logo=cloudflare&logoColor=white)](https://www.cloudflare.com/)
[![Tailscale](https://img.shields.io/badge/VPN-Tailscale-496495?style=flat-square&logo=tailscale&logoColor=white)](https://tailscale.com/)
[![Dockge](https://img.shields.io/badge/Stacks-Dockge-134e4a?style=flat-square&logo=docker&logoColor=white)](https://github.com/louislam/dockge)

---

```mermaid
flowchart TB
 subgraph subGraph0["Docker Network"]
        Dockge["🐳 Dockge UI"]
        NPM["🛡️ Nginx Proxy Manager"]
        Service1["App 1"]
  end
 subgraph subGraph1["TrueNAS Environment"]
        subGraph0
        Storage[("💾 ZFS Dataset")]
  end
    User(("🌐 Internet")) -- Domain Name --> Router["🏠 Home Router"]
    Router -- Port 80/443 --> NPM
    NPM -- Proxy Pass --> Dockge & Service1
    Dockge -- Manages --> Service1
    Service1 -. Mount .-> Storage
