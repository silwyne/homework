# DNS Server Setup with Docker

## Homework: Simple DNS Server Deployment

This document provides a minimal Docker Compose setup for running a DNS server using the official Bind9 image.

## Prerequisites
- Docker installed
- Docker Compose installed
- Basic terminal knowledge

## Step 1: Create Project Structure

Create a new directory for your DNS server:

```bash
mkdir dns-server
cd dns-server
```

## Step 2: Create DNS Configuration File


## Configuration Files

### 1. `docker-compose.yaml` file:

### 2. `config/named.conf`
```bind
// Main configuration file
include "/etc/bind/named.conf.options";
include "/etc/bind/named.conf.local";
```

### 3. `config/named.conf.options`
```bind
options {
        directory "/var/cache/bind";
        
        // Forward all queries to Google DNS
        forwarders {
                8.8.8.8;
                8.8.4.4;
        };
        
        // Only forward queries (don't try to resolve recursively ourselves)
        forward only;
        
        // Allow queries from anywhere (adjust if you want to restrict)
        allow-query { any; };
        
        // Disable recursion since we're forwarding (simpler and more secure)
        recursion no;
        
        // Listen on all interfaces
        listen-on { any; };
        listen-on-v6 { any; };
};
```

### 4. `config/named.conf.local`
```bind
// Zone for your local service domain
zone "myapp.local" {
        type primary;
        file "/etc/bind/zones/db.myapp.local";
        allow-update { none; };
};

// Optional: Reverse zone if you need PTR records
zone "168.192.in-addr.arpa" {
        type primary;
        file "/etc/bind/zones/db.192.168";
        allow-update { none; };
};
```

### 5. Zone file for your domain: `config/zones/db.myapp.local`
```bind
; BIND data file for myapp.local
$TTL    604800
@       IN      SOA     ns1.myapp.local. admin.myapp.local. (
                  2025022501   ; Serial (YYYYMMDDNN)
                  604800       ; Refresh
                  86400        ; Retry
                  2419200      ; Expire
                  604800 )     ; Negative Cache TTL

; Name server records
@       IN      NS      ns1.myapp.local.

; A record for the name server itself
ns1     IN      A       192.168.1.10   ; Replace with your Docker host IP

; Your service records
@       IN      A       192.168.1.20   ; myapp.local - main service IP
api     IN      A       192.168.1.21   ; api.myapp.local
db      IN      A       192.168.1.22   ; db.myapp.local
redis   IN      A       192.168.1.23   ; redis.myapp.local

; Optional: CNAME records
www     IN      CNAME   @              ; www.myapp.local -> myapp.local
```

### 6. Optional reverse zone: `config/zones/db.192.168`
This allows reverse lookups (getting hostname from IP). Only needed if you need PTR records.
```bind
; Reverse zone for 192.168.x.x
$TTL    604800
@       IN      SOA     ns1.myapp.local. admin.myapp.local. (
                  2025022501   ; Serial
                  604800       ; Refresh
                  86400        ; Retry
                  2419200      ; Expire
                  604800 )     ; Negative Cache TTL

; Name server
@       IN      NS      ns1.myapp.local.

; PTR records (reverse order: last octet first)
10      IN      PTR     ns1.myapp.local.      ; 192.168.1.10 -> ns1
20      IN      PTR     myapp.local.           ; 192.168.1.20 -> myapp.local
21      IN      PTR     api.myapp.local.       ; 192.168.1.21 -> api
22      IN      PTR     db.myapp.local.        ; 192.168.1.22 -> db
23      IN      PTR     redis.myapp.local.     ; 192.168.1.23 -> redis
```

## Directory Structure
```
your-project/
├── docker-compose.yml
├── config/
│   ├── named.conf
│   ├── named.conf.options
│   ├── named.conf.local
│   └── zones/
│       ├── db.myapp.local
│       └── db.192.168
├── cache/
└── logs/
```

## Setup Instructions

1. **Create the directory structure:**
```bash
mkdir -p config/zones cache logs
```

2. **Create all the configuration files** as shown above

3. **Adjust the IP addresses** in `db.myapp.local` to match your actual service IPs:
   - If services are on your host machine: use your host's local IP (e.g., 192.168.1.x)
   - If services are in Docker containers: use the container IPs or your host IP with port mapping

4. **Start the DNS server:**
```bash
docker-compose up -d
```

5. **Test the configuration:**
```bash
# Test forwarding (should resolve google.com)
dig @localhost google.com

# Test your local domain
dig @localhost myapp.local
dig @localhost api.myapp.local

# Test reverse lookup (if you set up the reverse zone)
dig @localhost -x 192.168.1.20
```

## Client Configuration

To use this DNS server from other machines/containers:

### For Docker containers:
Add this to their `docker-compose.yml`:
```yaml
services:
  your-service:
    dns:
      - 192.168.1.10  # IP of your Docker host running BIND
```

### For your host machine (Linux):
```bash
# Temporarily
sudo echo "nameserver 127.0.0.1" > /etc/resolv.conf

# Permanently (depends on your network manager)
# Edit /etc/resolv.conf or your network manager settings
```

### For Windows/Mac:
Set the DNS server in your network adapter settings to your Docker host's IP.

## Important Notes

1. **Serial Number**: Increment the serial number (YYYYMMDDNN) in zone files whenever you make changes
2. **Logs**: Check `logs/` directory for BIND logs if something doesn't work
3. **Firewall**: Make sure UDP/TCP port 53 is open if other machines need to access this DNS server
4. **Domain Name**: You can use any domain you want - `.local`, `.internal`, `.lan` are common choices for private networks

This setup gives you:
- ✅ Forwarding to Google DNS for all external queries
- ✅ Your own local domain (`myapp.local`) with custom records
- ✅ Simple and maintainable configuration
- ✅ Persistent cache and logs