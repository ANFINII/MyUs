class Author:
    def __init__(self, nickname: str, image: str, follower_count: int):
        self.nickname = nickname
        self.image = image
        self.follower_count = follower_count


class MediaUser:
    def __init__(self, nickname: str, image: str, is_like: int):
        self.nickname = nickname
        self.image = image
