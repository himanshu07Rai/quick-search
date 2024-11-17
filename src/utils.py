from enum import Enum
class SortByEnum(str, Enum):
    created_at = 'created_at'
    likes = 'likes'
    comments = 'comments'