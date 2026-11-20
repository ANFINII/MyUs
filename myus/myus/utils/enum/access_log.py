from enum import Enum


class AccessType(str, Enum):
    VIDEO = "Video"
    AUDIO = "Audio"
    BLOG = "Blog"
    COMIC = "Comic"
    PICTURE = "Picture"
    CHAT = "Chat"
    ADVERTISE = "Advertise"
