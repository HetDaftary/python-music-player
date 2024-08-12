import os
import subprocess

from PyQt5.QtCore import QThread 

class SinglePlaylistWindow(QThread):
    def __init__(self, playlistName, parent = None):
        super().__init__(parent)
        self.playlistName = playlistName
        self.running = True
        self.parent = parent
        self.parent.singleWindowRunning = True
        self.process = None

    def run(self):
        self.process = subprocess.Popen(["python3", "src/main.py", f"--single-playlist={self.playlistName}"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Keep the thread running while the subprocess is active
        while self.running:
            output = self.process.stdout.readline()
            error = self.process.stderr.readline()
        
            if output:
                print(f"STDOUT: {output.strip()}")
        
            if error:
                print(f"STDERR: {error.strip()}")
        
            # Break the loop if the process is done and there is no more output
            if output == '' and error == '' and self.process.poll() is not None:
                break
    
        # Ensure the process has finished
        #self.process.wait()

    def stop(self):
        # Kill the subprocess if it is still running
        if self.process and self.process.poll() is None:
            self.process.kill()
            self.process.wait()  # Wait for the process to terminate
            self.parent.singleWindowRunning = False
        self.running = False