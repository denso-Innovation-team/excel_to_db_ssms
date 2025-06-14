"""
security/auth_manager.py
Basic Authentication Manager for DENSO888
"""

import hashlib
import sqlite3
import json
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime, timedelta


class SimpleAuthManager:
    """Basic authentication manager for DENSO888"""
    
    def __init__(self, db_path: str = "auth.db"):
        self.db_path = Path(db_path)
        self.current_user: Optional[Dict[str, Any]] = None
        self._init_database()
    
    def _init_database(self):
        """Initialize authentication database"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    role TEXT DEFAULT 'user',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP,
                    active BOOLEAN DEFAULT 1
                )
            """)
            
            # Create default admin user if not exists
            admin_exists = conn.execute(
                "SELECT 1 FROM users WHERE username = 'admin'"
            ).fetchone()
            
            if not admin_exists:
                admin_hash = self._hash_password("admin123")
                conn.execute(
                    "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                    ("admin", admin_hash, "admin")
                )
    
    def _hash_password(self, password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def authenticate(self, username: str, password: str) -> bool:
        """Authenticate user credentials"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            
            user = conn.execute(
                "SELECT * FROM users WHERE username = ? AND active = 1",
                (username,)
            ).fetchone()
            
            if user and user['password_hash'] == self._hash_password(password):
                # Update last login
                conn.execute(
                    "UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?",
                    (user['id'],)
                )
                
                # Set current user
                self.current_user = dict(user)
                return True
        
        return False
    
    def logout(self):
        """Logout current user"""
        self.current_user = None
    
    def is_authenticated(self) -> bool:
        """Check if user is authenticated"""
        return self.current_user is not None
    
    def get_current_user(self) -> Optional[Dict[str, Any]]:
        """Get current authenticated user"""
        return self.current_user
    
    def has_permission(self, permission: str) -> bool:
        """Check if current user has permission"""
        if not self.current_user:
            return False
        
        # Simple role-based permissions
        role = self.current_user.get('role', 'user')
        
        admin_permissions = ['all']
        user_permissions = ['read', 'process', 'generate']
        
        if role == 'admin':
            return True
        elif role == 'user':
            return permission in user_permissions
        
        return False


# Global auth manager instance
auth_manager = SimpleAuthManager()


def require_auth(func):
    """Decorator to require authentication"""
    def wrapper(*args, **kwargs):
        if not auth_manager.is_authenticated():
            raise PermissionError("Authentication required")
        return func(*args, **kwargs)
    return wrapper


def require_permission(permission: str):
    """Decorator to require specific permission"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            if not auth_manager.has_permission(permission):
                raise PermissionError(f"Permission '{permission}' required")
            return func(*args, **kwargs)
        return wrapper
    return decorator
