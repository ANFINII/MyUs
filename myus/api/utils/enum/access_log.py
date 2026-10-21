from enum import Enum


class AccessType(str, Enum):
    VIDEO = "Video"
    MUSIC = "Music"
    BLOG = "Blog"
    COMIC = "Comic"
    PICTURE = "Picture"
    CHAT = "Chat"
    ADVERTISE = "Advertise"
