# app_models/__init__.py

from .user import User
from .role import Role
from .post import Post
from .comment import Comment

__all__ = ['User', 'Role', 'Post', 'Comment']
