"""Simple authentication"""

import hashlib
from typing import Optional, Tuple

class AuthManager:
    """Simple authentication manager"""
    
    def __init__(self):
        self.current_user = None
        self.users = {
            "admin": self._hash_password("admin123")
        }
    
    def _hash_password(self, password: str) -> str:
        """Hash password"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def authenticate(self, username: str, password: str) -> Tuple[bool, str]:
        """Authenticate user"""
        if username not in self.users:
            return False, "User not found"
            
        if self.users[username] != self._hash_password(password):
            return False, "Invalid password"
            
        self.current_user = username
        return True, "Login successful"
    
    def logout(self):
        """Logout user"""
        self.current_user = None
        
    def is_authenticated(self) -> bool:
        """Check if user is authenticated"""
        return self.current_user is not None
