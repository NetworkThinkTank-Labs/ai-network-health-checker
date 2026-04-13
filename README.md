# AI Network Health Checker

An AI-powered network health monitoring tool using **Python**, **Netmiko** for network device data collection, and **scikit-learn's Isolation Forest** for anomaly detection. Beginner-friendly project for network engineers.

Blog Post: [How I Built an AI Network Monitoring Tool (Beginner Friendly)](https://networkthinktank.blog/2025/04/13/how-i-built-an-ai-network-monitoring-tool-beginner-friendly/)

---

## What Does This Tool Do?

1. **Connects to network devices** via SSH using Netmiko
2. 2. **Collects interface statistics** - CRC errors, input/output errors, packet drops
   3. 3. **Feeds data into a machine learning model** (Isolation Forest) to detect anomalies
      4. 4. **Flags unhealthy interfaces** showing unusual behavior
        
         5. ---
        
         6. ## Project Structure
        
         7. ```
            ai-network-health-checker/
              network_collector.py      # Collects data from devices using Netmiko
              anomaly_detector.py       # Isolation Forest ML model for anomaly detection
              main.py                   # Main entry point
              devices.json              # Device inventory (IPs, credentials)
              requirements.txt          # Python dependencies
              .gitignore                # Git ignore rules
              README.md                 # This file
            ```

            ---

            ## Requirements

            - Python 3.8+
            - - Network devices accessible via SSH (or use demo mode)
              - - Libraries: netmiko, scikit-learn, pandas, numpy
               
                - ---

                ## Getting Started

                ### 1. Clone the Repository

                ```bash
                git clone https://github.com/NetworkThinkTank-Labs/ai-network-health-checker.git
                cd ai-network-health-checker
                ```

                ### 2. Install Dependencies

                ```bash
                pip install -r requirements.txt
                ```

                ### 3. Configure Your Devices

                Edit devices.json with your device info:

                ```json
                [
                  {
                    "device_type": "cisco_ios",
                    "host": "192.168.1.1",
                    "username": "admin",
                    "password": "password",
                    "secret": "enable_password"
                  }
                ]
                ```

                ### 4. Run the Tool

                ```bash
                python main.py
                ```

                ### 5. Demo Mode (No Devices Needed)

                ```bash
                python main.py --demo
                ```

                ---


                ## How It Works

                ### Data Collection (network_collector.py)
                - Uses Netmiko to SSH into each device
                - - Runs show interfaces to collect stats
                  - - Parses output for CRC errors, input/output errors, packet counts
                   
                    - ### Anomaly Detection (anomaly_detector.py)
                    - - Uses scikit-learn Isolation Forest algorithm
                      - - Trains on collected interface statistics
                        - - Labels each interface as normal or anomaly
                         
                          - ### Main Script (main.py)
                          - - Loads device inventory from devices.json
                            - - Collects data from all devices
                              - - Runs anomaly detection and outputs results
                               
                                - ---

                                ## Example Output

                                ```
                                Collecting data from devices...
                                  -> Connected to 192.168.1.1
                                  -> Connected to 192.168.1.2

                                Running anomaly detection...

                                Results:
                                Device             Interface        CRC     In Err    Out Err   Status
                                192.168.1.1        Gi0/0            0       0         0         Normal
                                192.168.1.1        Gi0/1            542     312       5         ANOMALY
                                192.168.1.2        Gi0/0            0       2         0         Normal

                                1 anomaly detected! Check Gi0/1 on 192.168.1.1.
                                ```

                                ---

                                ## Contributing

                                Contributions are welcome! Feel free to open issues or submit pull requests.

                                ## License

                                This project is licensed under the MIT License.

                                ## Resources

                                - [Blog Post](https://networkthinktank.blog/2025/04/13/how-i-built-an-ai-network-monitoring-tool-beginner-friendly/)
                                - - [Netmiko Documentation](https://github.com/ktbyers/netmiko)
                                  - - [scikit-learn Isolation Forest](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html)
                                    - - [NetworkThinkTank-Labs GitHub](https://github.com/NetworkThinkTank-Labs)
