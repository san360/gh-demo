#!/usr/bin/env python3
"""
Development server startup script for Insurance Products application.

This script starts both the Flask backend and Vite frontend development servers
in the correct order with proper error handling.
"""

import subprocess
import sys
import time
import threading
import os
from pathlib import Path


def run_backend():
    """Start the Flask backend server."""
    print("🚀 Starting Flask backend server...")
    
    # Change to backend directory
    backend_dir = Path(__file__).parent / "src" / "backend"
    
    try:
        process = subprocess.Popen(
            [sys.executable, "app.py"],
            cwd=backend_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        
        # Stream output
        for line in process.stdout:
            print(f"[Backend] {line.rstrip()}")
            
    except Exception as e:
        print(f"❌ Error starting backend: {e}")
        return False
    
    return True


def run_frontend():
    """Start the Vite frontend development server."""
    print("🚀 Starting Vite frontend server...")
    
    try:
        process = subprocess.Popen(
            ["npm", "run", "dev"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        
        # Stream output
        for line in process.stdout:
            print(f"[Frontend] {line.rstrip()}")
            
    except Exception as e:
        print(f"❌ Error starting frontend: {e}")
        return False
    
    return True


def check_dependencies():
    """Check if required dependencies are installed."""
    print("🔍 Checking dependencies...")
    
    # Check Python dependencies
    try:
        import flask
        import flask_cors
        print("✅ Python dependencies found")
    except ImportError as e:
        print(f"❌ Missing Python dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False
    
    # Check if node_modules exists
    if not os.path.exists("node_modules"):
        print("❌ Node.js dependencies not found")
        print("Please run: npm install")
        return False
    else:
        print("✅ Node.js dependencies found")
    
    return True


def main():
    """Main entry point for the development server."""
    print("Insurance Products Application - Development Server")
    print("=" * 50)
    
    # Check dependencies first
    if not check_dependencies():
        sys.exit(1)
    
    print("\n📋 Starting development servers...")
    print("Backend will be available at: http://localhost:5000")
    print("Frontend will be available at: http://localhost:3000")
    print("\nPress Ctrl+C to stop both servers\n")
    
    try:
        # Start backend in a separate thread
        backend_thread = threading.Thread(target=run_backend, daemon=True)
        backend_thread.start()
        
        # Give backend time to start
        time.sleep(3)
        
        # Start frontend (this will block)
        run_frontend()
        
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down development servers...")
        print("Goodbye! 👋")


if __name__ == "__main__":
    main()
