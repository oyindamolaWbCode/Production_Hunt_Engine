WITH reconciled_cases AS (
    SELECT 
        b.log_id AS raw_event_locator,
        b.timestamp AS exfil_time,
        b.bytes_sent,
        tickets.ticket_id AS controlling_record_id,
        CASE 
            WHEN tickets.ticket_id IS NULL OR tickets.status <> 'APPROVED' THEN 'MATERIAL_APPROVAL_MISMATCH'
            ELSE 'VALID_BENIGN_EVIDENCE'
        END AS case_classification
    FROM normalized_web_logs b
    LEFT JOIN controlling_change_records tickets 
        ON b.source_ip = tickets.target_ip
        AND b.timestamp BETWEEN tickets.window_start AND tickets.window_end
    WHERE b.bytes_sent > 52428800 
)
SELECT * FROM reconciled_cases
ORDER BY exfil_time ASC, raw_event_locator ASC;