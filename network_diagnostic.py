#!/usr/bin/env python3
"""
Network diagnostic script to troubleshoot IP webcam connection issues.
"""

import socket
import subprocess
import platform
import time
import urllib.request
import urllib.error

def ping_host(host):
    """Ping a host to check basic connectivity."""
    print(f"Pinging {host}...")
    
    try:
        # Use platform-specific ping command
        if platform.system().lower() == "windows":
            cmd = ["ping", "-n", "4", host]
        else:
            cmd = ["ping", "-c", "4", host]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print(f"✅ Ping to {host} successful")
            print(f"   Output: {result.stdout}")
        else:
            print(f"❌ Ping to {host} failed")
            print(f"   Error: {result.stderr}")
            
    except subprocess.TimeoutExpired:
        print(f"❌ Ping to {host} timed out")
    except Exception as e:
        print(f"❌ Ping error: {e}")

def test_port_connectivity(host, port):
    """Test if a specific port is open."""
    print(f"Testing port {port} on {host}...")
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        result = sock.connect_ex((host, port))
        sock.close()
        
        if result == 0:
            print(f"✅ Port {port} on {host} is open")
        else:
            print(f"❌ Port {port} on {host} is closed (error code: {result})")
            
    except Exception as e:
        print(f"❌ Port test error: {e}")

def test_http_endpoints(host, port):
    """Test various HTTP endpoints."""
    base_url = f"http://{host}:{port}"
    endpoints = ["/", "/shot.jpg", "/video", "/mjpeg", "/videofeed"]
    
    print(f"Testing HTTP endpoints on {base_url}...")
    
    for endpoint in endpoints:
        url = base_url + endpoint
        print(f"\nTesting: {url}")
        
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as response:
                print(f"  ✅ Status: {response.getcode()}")
                print(f"  ✅ Content-Type: {response.headers.get('Content-Type', 'Unknown')}")
                print(f"  ✅ Content-Length: {response.headers.get('Content-Length', 'Unknown')}")
                
                # Read a small amount of data
                data = response.read(1024)
                print(f"  ✅ Data received: {len(data)} bytes")
                
        except urllib.error.URLError as e:
            print(f"  ❌ HTTP Error: {e}")
        except Exception as e:
            print(f"  ❌ General Error: {e}")

def check_network_info():
    """Display network information."""
    print("Network Information:")
    print("=" * 50)
    
    try:
        # Get local IP
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        print(f"Hostname: {hostname}")
        print(f"Local IP: {local_ip}")
        
        # Get default gateway (Windows)
        if platform.system().lower() == "windows":
            try:
                result = subprocess.run(["ipconfig"], capture_output=True, text=True)
                print(f"Network config:\n{result.stdout}")
            except:
                pass
                
    except Exception as e:
        print(f"Error getting network info: {e}")

def main():
    host = "10.133.243.8"
    port = 8080
    
    print("Network Diagnostic Tool")
    print("=" * 50)
    
    # Check network information
    check_network_info()
    
    print(f"\nDiagnosing connection to {host}:{port}")
    print("=" * 50)
    
    # Test basic connectivity
    ping_host(host)
    
    # Test port connectivity
    test_port_connectivity(host, port)
    
    # Test HTTP endpoints
    test_http_endpoints(host, port)
    
    print("\n" + "=" * 50)
    print("Diagnostic completed!")
    print("\nTroubleshooting tips:")
    print("1. Make sure the IP webcam app is running on the device")
    print("2. Check if the device is on the same network")
    print("3. Verify the IP address is correct")
    print("4. Check firewall settings")
    print("5. Try using the device's local IP address instead")

if __name__ == "__main__":
    main() 