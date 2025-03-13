import psutil
import ctypes

# Define Windows API functions
kernel32 = ctypes.windll.kernel32

# Constants
PROCESS_ALL_ACCESS = 0x1F0FFF
MEM_COMMIT = 0x1000
MEM_RESERVE = 0x2000
PAGE_READWRITE = 0x04
CREATE_SUSPENDED = 0x04
THREAD_CREATE = 0x0002

# Define required Windows functions
OpenProcess = kernel32.OpenProcess
VirtualAllocEx = kernel32.VirtualAllocEx
WriteProcessMemory = kernel32.WriteProcessMemory
CreateRemoteThread = kernel32.CreateRemoteThread
GetModuleHandleA = kernel32.GetModuleHandleA
LoadLibraryA = kernel32.GetProcAddress(GetModuleHandleA(b"kernel32.dll"), b"LoadLibraryA")

def find_process_pid(process_name: str) -> int:
    """Find process ID (PID) by name."""
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'].lower() == process_name.lower():
            return proc.info['pid']
    return None