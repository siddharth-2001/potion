from redis import Redis


class AuthRetryService:

    RETRY_TABLE_NAME = "auth-retry"
    MAX_RETRIES = 3

    def __init__(self, redis: Redis) -> None:
        self.redis = redis

    def get_retry_count(self, user_id: str) -> int:
        return int(self.redis.hget(self.RETRY_TABLE_NAME, user_id))  # type:ignore

    def increment_retry_count(self, user_id: str):

        retries = self.redis.hincrby(self.RETRY_TABLE_NAME, user_id, 1)

        if retries > self.MAX_RETRIES: # type: ignore
            raise Exception("Too many login attempts")
