"""
network_collector.py
Collects interface statistics from network devices using Netmiko.
"""

import re
import json
from netmiko import ConnectHandler


def load_devices(filepath="devices.json"):
      """Load device inventory from a JSON file."""
      with open(filepath, "r") as f:
                devices = json.load(f)
            return devices


def collect_interface_stats(device_params):
      """Connect to a network device and collect interface statistics."""
    stats = []
    try:
              print(f"  -> Connecting to {device_params['host']}...")
              connection = ConnectHandler(**device_params)
              output = connection.send_command("show interfaces")
              stats = parse_interface_output(output, device_params["host"])
              connection.disconnect()
              print(f"  -> Collected stats from {device_params['host']} ({len(stats)} interfaces)")
except Exception as e:
        print(f"  x Error connecting to {device_params['host']}: {e}")
    return stats


def parse_interface_output(output, device_ip):
      """Parse show interfaces output to extract key metrics."""
    interfaces = []
    interface_blocks = re.split(r"(?=^\S+\s+is\s+)", output, flags=re.MULTILINE)

    for block in interface_blocks:
              if not block.strip():
                            continue
                        name_match = re.match(r"^(\S+)\s+is\s+(up|down|administratively down)", block)
        if not name_match:
                      continue

        interface_name = name_match.group(1)
        status = name_match.group(2)

        crc_errors = extract_metric(block, r"(\d+)\s+CRC")
        input_errors = extract_metric(block, r"(\d+)\s+input errors")
        output_errors = extract_metric(block, r"(\d+)\s+output errors")
        input_packets = extract_metric(block, r"(\d+)\s+packets input")
        output_packets = extract_metric(block, r"(\d+)\s+packets output")

        interfaces.append({
                      "device": device_ip,
                      "interface": interface_name,
                      "status": status,
                      "crc_errors": crc_errors,
                      "input_errors": input_errors,
                      "output_errors": output_errors,
                      "input_packets": input_packets,
                      "output_packets": output_packets,
        })
    return interfaces


def extract_metric(text, pattern):
      """Extract a numeric metric from text using a regex pattern."""
    match = re.search(pattern, text)
    return int(match.group(1)) if match else 0


def collect_all_devices(devices):
      """Collect interface stats from all devices in the inventory."""
    all_stats = []
    for device in devices:
              stats = collect_interface_stats(device)
        all_stats.extend(stats)
    return all_stats


def generate_demo_data():
      """Generate simulated interface statistics for testing."""
    import random

    demo_data = []
    devices = ["192.168.1.1", "192.168.1.2", "10.0.0.1"]
    ifaces = ["GigabitEthernet0/0", "GigabitEthernet0/1", "GigabitEthernet0/2", "GigabitEthernet0/3"]

    for device in devices:
              for iface in ifaces:
                            demo_data.append({
                                              "device": device,
                                              "interface": iface,
                                              "status": "up",
                                              "crc_errors": random.randint(0, 5),
                                              "input_errors": random.randint(0, 10),
                                              "output_errors": random.randint(0, 3),
                                              "input_packets": random.randint(50000, 500000),
                                              "output_packets": random.randint(50000, 500000),
                            })

    # Inject anomalies
    demo_data[1]["crc_errors"] = 542
    demo_data[1]["input_errors"] = 312
    demo_data[7]["crc_errors"] = 128
    demo_data[7]["input_errors"] = 87

    return demo_data
