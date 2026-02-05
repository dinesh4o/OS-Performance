import psutil
import database

def get_system_metrics():
    """Collects current system metrics."""
    # CPU usage (interval=None is important to not block, but requires a previous call or interval in loop)
    # We will use interval=0.1 for a quick blocking check which is acceptable for this use case
    cpu = psutil.cpu_percent(interval=0.1)
    
    # RAM usage
    ram = psutil.virtual_memory().percent
    
    # Disk usage (root)
    disk = psutil.disk_usage('/').percent
    
    # Process count
    processes = len(psutil.pids())

    # Get Top CPU Process
    top_pid = None
    top_name = "None"
    top_cpu = 0
    try:
        # Iterate over all running processes
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
            try:
                p_cpu = proc.info['cpu_percent']
                # psutil cpu_percent can be 0.0 on first call or > 100 on multi-core
                if p_cpu and p_cpu > top_cpu:
                    top_cpu = p_cpu
                    top_name = proc.info['name']
                    top_pid = proc.info['pid']
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
    except Exception as e:
        pass # Fail gracefully
    
    return {
        'cpu': cpu,
        'ram': ram,
        'disk': disk,
        'processes': processes,
        'top_process': {'name': top_name, 'cpu': top_cpu, 'pid': top_pid}
    }

def get_process_list():
    """Returns list of running processes for Task Manager view. 
       Uses a 1.0s sampling interval with PERSISTENT process objects for accurate CPU readings.
    """
    import time
    procs = []
    
    # Dictionary to store process objects: {pid: process_obj}
    proc_map = {}
    
    # 1. First Pass: snapshot all running processes and "prime" their CPU counters
    try:
        for p in psutil.process_iter(['pid', 'name', 'username', 'memory_info']):
            try:
                # Prime the CPU counter (returns 0.0 or random first value)
                p.cpu_percent(interval=None)
                proc_map[p.pid] = p
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
    except Exception:
        pass

    # 2. Wait for sampling window (1.0s for stability)
    time.sleep(1.0)

    # 3. Second Pass: Re-use the SAME objects to get the delta
    for pid, p in proc_map.items():
        try:
            # Check if process is still running and get validity
            if p.is_running():
                # cpu_percent on the SAME object returns usage since last call (approx 1s ago)
                cpu_val = p.cpu_percent(interval=None)
                
                # Normalize by core count so 100% = Full System Load (optional, but requested for "realism")
                # Remove this division if you want "Task Manager" style where 100% = 1 Core on multi-core
                # standard Task Manager shows total CPU % relative to ALL cores.
                # psutil returns percentage per core.
                cpu_val = cpu_val / psutil.cpu_count()

                mem_mb = p.memory_info().rss / (1024 * 1024)
                
                procs.append({
                    'pid': pid,
                    'name': p.name(),
                    'cpu': round(cpu_val, 1),
                    'memory': round(mem_mb, 1)
                })
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    
    # Sort by memory usage desc
    return sorted(procs, key=lambda x: x['memory'], reverse=True)[:50] # Top 50

def collect_and_store():
    """Gets metrics and stores them in DB."""
    data = get_system_metrics()
    database.insert_metric(data['cpu'], data['ram'], data['disk'], data['processes'])
    return data
