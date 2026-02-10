// Stub for anti-debug detection
// This is a placeholder stub that can be integrated into the APK hardening process
// It provides basic detection for debugging attempts

package com.hardening.stubs;

import android.content.Context;
import android.os.Debug;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

public class AntiDebug {
    
    /**
     * Check if debugger is connected
     * @return true if debugger is detected
     */
    public static boolean isDebuggerConnected() {
        return Debug.isDebuggerConnected();
    }
    
    /**
     * Check if app is debuggable via ApplicationInfo
     * @param context Application context
     * @return true if app is debuggable
     */
    public static boolean isDebuggable(Context context) {
        return (context.getApplicationInfo().flags & android.content.pm.ApplicationInfo.FLAG_DEBUGGABLE) != 0;
    }
    
    /**
     * Check for TracerPid in /proc/self/status
     * @return true if a tracer is detected
     */
    public static boolean isTracerPresent() {
        try {
            BufferedReader reader = new BufferedReader(new FileReader("/proc/self/status"));
            String line;
            while ((line = reader.readLine()) != null) {
                if (line.startsWith("TracerPid:")) {
                    String[] parts = line.split(":");
                    if (parts.length > 1) {
                        int tracerPid = Integer.parseInt(parts[1].trim());
                        reader.close();
                        return tracerPid != 0;
                    }
                }
            }
            reader.close();
        } catch (IOException | NumberFormatException e) {
            // Error reading status file
        }
        return false;
    }
    
    /**
     * Perform timing check to detect debugging
     * Debuggers typically slow down execution
     * @return true if timing suggests debugging
     */
    public static boolean isTimingAnomaly() {
        long start = System.currentTimeMillis();
        // Simple operation
        for (int i = 0; i < 1000; i++) {
            Math.sqrt(i);
        }
        long end = System.currentTimeMillis();
        long duration = end - start;
        
        // If operation took unusually long, might be debugging
        return duration > 100;
    }
    
    /**
     * Comprehensive debug detection
     * @param context Application context
     * @return true if debugging is detected
     */
    public static boolean isBeingDebugged(Context context) {
        return isDebuggerConnected() 
            || isDebuggable(context) 
            || isTracerPresent() 
            || isTimingAnomaly();
    }
    
    /**
     * Anti-debug check that can terminate the app
     * @param context Application context
     */
    public static void enforceAntiDebug(Context context) {
        if (isBeingDebugged(context)) {
            // In production, this might exit the app or corrupt data
            android.os.Process.killProcess(android.os.Process.myPid());
        }
    }
}
