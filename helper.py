import ctypes
from ctypes import wintypes
import pyMeow as pm

# Constants and Structures
TH32CS_SNAPPROCESS = 0x00000002
TH32CS_SNAPTHREAD = 0x00000004
THREAD_QUERY_LIMITED_INFORMATION = 0x0800
THREAD_TERMINATE = 0x0001

class PROCESSENTRY32(ctypes.Structure):
    _fields_ = [
        ("dwSize", wintypes.DWORD),
        ("cntUsage", wintypes.DWORD),
        ("th32ProcessID", wintypes.DWORD),
        ("th32DefaultHeapID", wintypes.ULONG),
        ("th32ModuleID", wintypes.DWORD),
        ("cntThreads", wintypes.DWORD),
        ("th32ParentProcessID", wintypes.DWORD),
        ("pcPriClassBase", wintypes.LONG),
        ("dwFlags", wintypes.DWORD),
        ("szExeFile", wintypes.CHAR * 260)
    ]

class THREADENTRY32(ctypes.Structure):
    _fields_ = [
        ("dwSize", wintypes.DWORD),
        ("cntUsage", wintypes.DWORD),
        ("th32ThreadID", wintypes.DWORD),
        ("th32OwnerProcessID", wintypes.DWORD),
        ("tpBasePri", wintypes.LONG),
        ("tpDeltaPri", wintypes.LONG),
        ("dwFlags", wintypes.DWORD)
    ]

# API Setup
kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)

# Process/Thread Enumeration
kernel32.CreateToolhelp32Snapshot.argtypes = [wintypes.DWORD, wintypes.DWORD]
kernel32.CreateToolhelp32Snapshot.restype = wintypes.HANDLE

kernel32.Process32First.argtypes = [wintypes.HANDLE, ctypes.POINTER(PROCESSENTRY32)]
kernel32.Process32First.restype = wintypes.BOOL

kernel32.Process32Next.argtypes = [wintypes.HANDLE, ctypes.POINTER(PROCESSENTRY32)]
kernel32.Process32Next.restype = wintypes.BOOL

kernel32.Thread32First.argtypes = [wintypes.HANDLE, ctypes.POINTER(THREADENTRY32)]
kernel32.Thread32First.restype = wintypes.BOOL

kernel32.Thread32Next.argtypes = [wintypes.HANDLE, ctypes.POINTER(THREADENTRY32)]
kernel32.Thread32Next.restype = wintypes.BOOL

# Thread Operations
kernel32.OpenThread.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
kernel32.OpenThread.restype = wintypes.HANDLE

kernel32.GetThreadDescription.argtypes = [wintypes.HANDLE, ctypes.POINTER(ctypes.c_wchar_p)]
kernel32.GetThreadDescription.restype = wintypes.BOOL

kernel32.TerminateThread.argtypes = [wintypes.HANDLE, wintypes.DWORD]
kernel32.TerminateThread.restype = wintypes.BOOL

kernel32.CloseHandle.argtypes = [wintypes.HANDLE]
kernel32.CloseHandle.restype = wintypes.BOOL

def get_process_id(process_name):
    
    return pm.open_process(process_name)["pid"]

def terminate_thread_by_name(process_name, thread_name):
    pid = get_process_id(process_name)
    if not pid:
        print(f"Process {process_name} not found")
        return False

    h_snapshot = kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPTHREAD, 0)
    if h_snapshot == -1:
        return False

    entry = THREADENTRY32()
    entry.dwSize = ctypes.sizeof(THREADENTRY32)
    
    if not kernel32.Thread32First(h_snapshot, ctypes.byref(entry)):
        kernel32.CloseHandle(h_snapshot)
        return False

    target_thread_id = None
    
    while True:
        if entry.th32OwnerProcessID == pid:
            h_thread = kernel32.OpenThread(THREAD_QUERY_LIMITED_INFORMATION, False, entry.th32ThreadID)
            if h_thread:
                name_ptr = ctypes.c_wchar_p()
                if kernel32.GetThreadDescription(h_thread, ctypes.byref(name_ptr)):
                    current_name = name_ptr.value
                    if current_name and thread_name in current_name:
                        print(f"Found thread '{current_name}' in {process_name}")
                        target_thread_id = entry.th32ThreadID
                        kernel32.CloseHandle(h_thread)
                        break
                kernel32.CloseHandle(h_thread)
        if not kernel32.Thread32Next(h_snapshot, ctypes.byref(entry)):
            break

    kernel32.CloseHandle(h_snapshot)

    if not target_thread_id:
        print(f"Thread with name '{thread_name}' not found in {process_name}")
        return False

    # Terminate the found thread
    h_thread = kernel32.OpenThread(THREAD_TERMINATE, False, target_thread_id)
    if not h_thread:
        print(f"Failed to open thread (Error: {ctypes.get_last_error()})")
        return False

    if not kernel32.TerminateThread(h_thread, 0):
        print(f"Failed to terminate thread (Error: {ctypes.get_last_error()})")
        kernel32.CloseHandle(h_thread)
        return False

    kernel32.CloseHandle(h_thread)
    print(f"Successfully terminated thread '{thread_name}' (ID: {target_thread_id})")
    return True
