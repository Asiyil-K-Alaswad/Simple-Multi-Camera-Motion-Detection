#!/usr/bin/env python3
"""
Script to find the correct port for IP webcam.
"""

import socket
import urllib.request
import urllib.error
import time

def test_port(ip, port):
    """Test if a port is open and has webcam service."""
    try:
        # Test TCP connection
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        result = sock.connect_ex((ip, port))
        sock.close()
        
        if result == 0:
            # Port is open, test HTTP endpoints
            return test_http_endpoints(ip, port)
        else:
            return False, f"Port {port} closed (error: {result})"
            
    except Exception as e:
        return False, f"Error testing port {port}: {e}"

def test_http_endpoints(ip, port):
    """Test common IP webcam HTTP endpoints."""
    base_url = f"http://{ip}:{port}"
    endpoints = ["/", "/shot.jpg", "/video", "/mjpeg", "/videofeed", "/stream"]
    
    for endpoint in endpoints:
        url = base_url + endpoint
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as response:
                if response.getcode() == 200:
                    content_type = response.headers.get('Content-Type', '')
                    content_length = response.headers.get('Content-Length', 'Unknown')
                    return True, f"✅ Found webcam at {url} (Content-Type: {content_type}, Length: {content_length})"
        except:
            continue
    
    return False, f"Port {port} open but no webcam endpoints found"

def main():
    """Main function."""
    target_ip = "192.168.238.47"
    
    print(f"Scanning for IP webcam on {target_ip}...")
    print("=" * 60)
    
    # Common IP webcam ports
    ports = [8080, 8081, 8082, 8000, 8888, 9000, 8083, 8084, 8085, 8086, 8087, 8088, 8089, 8090]
    
    found_webcams = []
    
    for port in ports:
        print(f"Testing port {port}...", end=" ")
        success, message = test_port(target_ip, port)
        
        if success:
            print(f"✅ {message}")
            found_webcams.append((port, message))
        else:
            print(f"❌ {message}")
    
    print("\n" + "=" * 60)
    if found_webcams:
        print("Found IP webcam(s):")
        for port, message in found_webcams:
            print(f"  Port {port}: {message}")
        
        print("\nTo use with the tracking script, update the URL to:")
        for port, _ in found_webcams:
            print(f"  http://{target_ip}:{port}/shot.jpg")
    else:
        print("No IP webcam found on common ports.")
        print("\nTroubleshooting:")
        print("1. Make sure the IP webcam app is running on the device")
        print("2. Check what port the app is using")
        print("3. Try accessing the webcam URL in a browser")
        print("4. Check if there's a firewall blocking the connection")

if __name__ == "__main__":
    main() 