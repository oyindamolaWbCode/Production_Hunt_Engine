# SOC Shift Continuity Record
**Evidence Marker:** UBI-A5-3A20CEDE0A6A

## Campaign 1: Lateral Movement Velocity
*   **Rejected Hypothesis:** Actor utilizing Pass-the-Hash across Windows AD.
*   **Reason:** Cross-referencing `auth_logs` with `firewall_logs` proved lateral movement occurred exclusively over SSH between Linux servers.
*   **Next Collection Action:** Deploy auditd telemetry on the Linux web tier to capture exact bash commands.

## Campaign 2: Data Exfiltration
*   **Rejected Hypothesis:** Large outbound spikes were routine database backups.
*   **Reason:** Reconciling egress against `controlling_change_records` identified instances occurring outside approved maintenance windows.
*   **Next Collection Action:** Request SSL/TLS decryption logs from the perimeter firewall to inspect payload contents.