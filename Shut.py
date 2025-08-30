import time
import os
import sys
import platform
from datetime import datetime

class SystemShutdown:
    def __init__(self):
        self.system = platform.system()
        
    def get_current_epoch(self):
        """Get current epoch time"""
        return int(time.time())
    
    def epoch_to_datetime(self, epoch_time):
        """Convert epoch to readable datetime"""
        return datetime.fromtimestamp(epoch_time)
    
    def datetime_to_epoch(self, dt_string):
        """Convert datetime string to epoch"""
        try:
            dt = datetime.strptime(dt_string, "%Y-%m-%d %H:%M:%S")
            return int(dt.timestamp())
        except ValueError:
            return None
    
    def validate_future_time(self, target_epoch):
        """Check if the target time is in the future"""
        current_epoch = self.get_current_epoch()
        return target_epoch > current_epoch
    
    def shutdown_system(self):
        """Execute system shutdown command based on OS"""
        try:
            if self.system == "Windows":
                os.system("shutdown /s /t 1")
            elif self.system == "Linux" or self.system == "Darwin":  # Darwin is macOS
                os.system("sudo shutdown -h now")
            else:
                print(f"Unsupported operating system: {self.system}")
                return False
            return True
        except Exception as e:
            print(f"Error executing shutdown: {e}")
            return False
    
    def countdown_display(self, target_epoch):
        """Display countdown until shutdown"""
        while True:
            current_epoch = self.get_current_epoch()
            remaining_seconds = target_epoch - current_epoch
            
            if remaining_seconds <= 0:
                print("\n🔴 Time's up! Shutting down system...")
                return True
            
            # Convert remaining seconds to hours, minutes, seconds
            hours = remaining_seconds // 3600
            minutes = (remaining_seconds % 3600) // 60
            seconds = remaining_seconds % 60
            
            # Clear line and show countdown
            print(f"\r⏰ Shutdown in: {hours:02d}:{minutes:02d}:{seconds:02d}", end="", flush=True)
            time.sleep(1)
    
    def get_user_input(self):
        """Get shutdown time from user"""
        print("🚀 System Shutdown Scheduler")
        print("=" * 40)
        print(f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Current epoch: {self.get_current_epoch()}")
        print("\nChoose input method:")
        print("1. Enter epoch timestamp directly")
        print("2. Enter datetime (YYYY-MM-DD HH:MM:SS)")
        print("3. Set minutes from now")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            return self.get_epoch_input()
        elif choice == "2":
            return self.get_datetime_input()
        elif choice == "3":
            return self.get_minutes_input()
        else:
            print("❌ Invalid choice!")
            return None
    
    def get_epoch_input(self):
        """Get epoch timestamp from user"""
        try:
            epoch_input = input("Enter epoch timestamp: ").strip()
            target_epoch = int(epoch_input)
            
            if not self.validate_future_time(target_epoch):
                print("❌ Time must be in the future!")
                return None
                
            target_datetime = self.epoch_to_datetime(target_epoch)
            print(f"✅ Shutdown scheduled for: {target_datetime}")
            return target_epoch
            
        except ValueError:
            print("❌ Invalid epoch timestamp!")
            return None
    
    def get_datetime_input(self):
        """Get datetime from user and convert to epoch"""
        datetime_input = input("Enter datetime (YYYY-MM-DD HH:MM:SS): ").strip()
        target_epoch = self.datetime_to_epoch(datetime_input)
        
        if target_epoch is None:
            print("❌ Invalid datetime format!")
            return None
        
        if not self.validate_future_time(target_epoch):
            print("❌ Time must be in the future!")
            return None
        
        print(f"✅ Shutdown scheduled for: {datetime_input}")
        print(f"✅ Epoch timestamp: {target_epoch}")
        return target_epoch
    
    def get_minutes_input(self):
        """Get minutes from now and convert to epoch"""
        try:
            minutes = int(input("Enter minutes from now: ").strip())
            if minutes <= 0:
                print("❌ Minutes must be positive!")
                return None
            
            target_epoch = self.get_current_epoch() + (minutes * 60)
            target_datetime = self.epoch_to_datetime(target_epoch)
            print(f"✅ Shutdown scheduled for: {target_datetime}")
            print(f"✅ Epoch timestamp: {target_epoch}")
            return target_epoch
            
        except ValueError:
            print("❌ Invalid number!")
            return None
    
    def run(self):
        """Main execution method"""
        try:
            target_epoch = self.get_user_input()
            
            if target_epoch is None:
                print("❌ Failed to set shutdown time!")
                return
            
            # Confirmation
            confirm = input(f"\n⚠️  Confirm shutdown at {self.epoch_to_datetime(target_epoch)}? (y/N): ").strip().lower()
            
            if confirm != 'y':
                print("❌ Shutdown cancelled!")
                return
            
            print(f"\n✅ Shutdown scheduled successfully!")
            print("Press Ctrl+C to cancel...")
            
            # Start countdown
            if self.countdown_display(target_epoch):
                self.shutdown_system()
                
        except KeyboardInterrupt:
            print("\n\n❌ Shutdown cancelled by user!")
        except Exception as e:
            print(f"\n❌ An error occurred: {e}")

# Usage Example
if __name__ == "__main__":
    # Check if running with appropriate permissions
    if platform.system() in ["Linux", "Darwin"]:
        if os.geteuid() != 0:
            print("⚠️  Note: You may need to run with sudo for shutdown to work on Unix systems")
    
    scheduler = SystemShutdown()
    scheduler.run()
