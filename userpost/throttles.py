from rest_framework.throttling import UserRateThrottle


class PostLikeThrottle(UserRateThrottle):
    rate = '2/min'

class PostCommentThrottle(UserRateThrottle):
    rate = '2/min'