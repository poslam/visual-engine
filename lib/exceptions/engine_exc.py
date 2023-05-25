class EngineException(Exception):
    NOT_FOUND_ERROR = lambda x: f"{x} not found"
    COLLISION_ERROR = "engine has a collision with entities id's"
    DIRECTION_ERROR = "this object doesn't have direction to do this operation"
    ROOT_PROPERTY = "trying to access root property"
    WRONG_INPUT = "trying to input data, that's not allowed"