#!/usr/bin/env python3
"""
Script to find IP webcam devices on the local network.
"""

import socket
import threading
import time
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed

def scan_port(ip, port):
    """Scan a specific IP and port."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex((ip, port))
        sock.close()
        return result == 0
    except:
        return False

def test_http_endpoint(ip, port):
    """Test if an IP has an HTTP webcam endpoint."""
    url = f"http://{ip}:{port}/shot.jpg"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=3) as response:
            if response.getcode() == 200:
                content_type = response.headers.get('Content-Type', '')
                if 'image' in content_type.lower() or 'jpeg' in content_type.lower():
                    return True, f"✅ Found IP webcam at {ip}:{port} (Content-Type: {content_type})"
    except:
        pass
    return False, ""

def scan_network():
    """Scan the local network for IP webcam devices."""
    print("Scanning local network for IP webcam devices...")
    print("=" * 60)
    
    # Get local IP and determine network range
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        print(f"Your local IP: {local_ip}")
        
        # Extract network prefix (assuming /24 subnet)
        ip_parts = local_ip.split('.')
        network_prefix = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}"
        print(f"Scanning network: {network_prefix}.0/24")
        
    except Exception as e:
        print(f"Error getting local IP: {e}")
        return
    
    # Common ports for IP webcams
    ports = [8080, 8081, 8082, 8000, 8888, 9000]
    
    found_devices = []
    
    # Scan all IPs in the network
    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = []
        
        for i in range(1, 255):
            ip = f"{network_prefix}.{i}"
            
            # Skip our own IP
            if ip == local_ip:
                continue
                
            for port in ports:
                futures.append(executor.submit(scan_port, ip, port))
                futures.append(executor.submit(test_http_endpoint, ip, port))
        
        # Process results
        for future in as_completed(futures):
            try:
                result = future.result()
                if isinstance(result, tuple) and result[0]:  # HTTP endpoint found
                    found_devices.append(result[1])
                    print(result[1])
            except Exception as e:
                pass
    
    print("\n" + "=" * 60)
    if found_devices:
        print("Found IP webcam devices:")
        for device in found_devices:
            print(f"  {device}")
    else:
        print("No IP webcam devices found on the network.")
        print("\nTroubleshooting tips:")
        print("1. Make sure your IP webcam app is running")
        print("2. Check that the device is on the same WiFi network")
        print("3. Try different ports (8080, 8081, 8000, etc.)")
        print("4. Check the IP address shown in your IP webcam app")

if __name__ == "__main__":
    scan_network() 