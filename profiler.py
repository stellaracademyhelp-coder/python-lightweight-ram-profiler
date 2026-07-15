import os
import sys
import csv
import time

def parse_proc_meminfo():
    """
    Reads /proc/meminfo directly. Works natively on Android and Linux
    without requiring any compiled C extensions.
    """
    try:
        with open('/proc/meminfo', 'r') as f:
            lines = f.readlines()
        
        mem_info = {}
        for line in lines:
            parts = line.split()
            if len(parts) >= 2:
                key = parts[0].strip(':')
                val = int(parts[1])  # Raw value in kB
                mem_info[key] = val
        
        if 'MemTotal' in mem_info:
            total_kb = mem_info['MemTotal']
            
            # MemAvailable represents real-world free memory (cache-aware)
            if 'MemAvailable' in mem_info:
                avail_kb = mem_info['MemAvailable']
            else:
                # Fallback for older Linux/Android kernels
                free = mem_info.get('MemFree', 0)
                buffers = mem_info.get('Buffers', 0)
                cached = mem_info.get('Cached', 0)
                avail_kb = free + buffers + cached
                
            used_kb = total_kb - avail_kb
            percent_used = (used_kb / total_kb) * 100
            
            # Convert kB to Gigabytes (1 GB = 1024 * 1024 kB)
            total_gb = total_kb / 1048576
            used_gb = used_kb / 1048576
            
            return total_gb, used_gb, percent_used
    except FileNotFoundError:
        return None
    except Exception:
        return None

def get_ram_usage():
    """
    Cross-platform RAM monitor:
    1. Tries psutil (Standard for desktop)
    2. Falls back to pure-Python /proc/meminfo (Perfect for Android/Pydroid)
    3. Final static mock fallback to prevent crashes
    """
    try:
        import psutil
        vm = psutil.virtual_memory()
        total_gb = vm.total / (1024 ** 3)
        used_gb = vm.used / (1024 ** 3)
        return total_gb, used_gb, vm.percent
    except ImportError:
        pass
    
    stats = parse_proc_meminfo()
    if stats is not None:
        return stats
    
    return 8.0, 0.0, 0.0

def monitor_ram(duration_seconds=20, interval_seconds=1, output_file="ram_telemetry_log.csv"):
    """Logs system RAM usage to the console and exports it to a CSV file."""
    print(f"[*] Initializing telemetry run...")
    print(f"[*] Log file destination: {os.path.abspath(output_file)}")
    print(f"\n{'Timestamp':<10} | {'Total RAM':<12} | {'Used RAM':<12} | {'Usage %':<10}")
    print("-" * 55)
    
    log_dir = os.path.dirname(output_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)
        
    with open(output_file, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Timestamp", "Total_RAM_GB", "Used_RAM_GB", "Percentage_Used"])
        
        start_time = time.time()
        try:
            while time.time() - start_time < duration_seconds:
                total, used, percent = get_ram_usage()
                current_time = time.strftime("%H:%M:%S")
                
                print(f"{current_time:<10} | {total:>9.2f} GB | {used:>9.2f} GB | {percent:>8.1f}%")
                
                writer.writerow([current_time, round(total, 2), round(used, 2), round(percent, 1)])
                f.flush()
                
                time.sleep(interval_seconds)
        except KeyboardInterrupt:
            print("\n[-] Logging paused by user request.")
            
    print(f"\n[+] Telemetry complete! Saved to {output_file}")

if __name__ == "__main__":
    monitor_ram(duration_seconds=20, interval_seconds=1)
          
