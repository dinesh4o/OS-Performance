def get_recommendation(load_status, cpu, ram, disk, top_process=None):
    """Generates a decision-support recommendation."""
    
    recommendations = []
    
    if load_status == "High Load":
        recommendations.append("CRITICAL: System is under heavy strain.")
        
        # Specific Process Recommendation
        if top_process and top_process['cpu'] > 20: # Threshold for "significant" usage
            recommendations.append(f"HIGH LOAD DETECTED: Process '{top_process['name']}' (PID: {top_process['pid']}) is using {top_process['cpu']}% CPU. Recommend terminating if unused.")
            
        if cpu > 80:
            recommendations.append("- High CPU usage detected. Consider closing CPU-intensive background applications.")
        if ram > 80:
            recommendations.append("- Memory is critical. Close unused browser tabs or Electron apps.")
        if disk > 90:
            recommendations.append("- Disk space near capacity. Run disk cleanup or move large files to external storage.")
            
    elif load_status == "Medium Load":
        recommendations.append("WARNING: System is under moderate load.")
        
        if top_process and top_process['cpu'] > 15:
             recommendations.append(f"Performance Tip: Process '{top_process['name']}' is using significant CPU ({top_process['cpu']}%)")

        if ram > 60:
            recommendations.append("- RAM usage is climbing. Monitor browser usage.")
        if cpu > 50:
             recommendations.append("- CPU usage is noticeable. Check for background updates.")
             
    else:
        if top_process and top_process['cpu'] > 10 and top_process['name'] != 'System Idle Process':
             recommendations.append(f"Observation: '{top_process['name']}' is the active task ({top_process['cpu']}%)")
        recommendations.append("System is running optimally. No action needed.")
        
    return recommendations
