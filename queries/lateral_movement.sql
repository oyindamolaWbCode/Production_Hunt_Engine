WITH correlated_network_edges AS (
    SELECT 
        auth.global_actor_id,
        auth.timestamp AS auth_time,
        auth.log_id AS source_locator_1,
        net.log_id AS source_locator_2
    FROM normalized_auth_logs auth
    JOIN normalized_firewall_logs net 
        ON net.source_ip = auth.source_ip 
    WHERE net.timestamp BETWEEN auth.timestamp - INTERVAL '5 Minutes' AND auth.timestamp
)
SELECT * FROM correlated_network_edges
ORDER BY auth_time ASC, source_locator_1 ASC;