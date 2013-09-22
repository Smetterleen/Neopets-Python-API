class IslandTrainingSchoolException(Exception):
    pass

class UnknownStatException(IslandTrainingSchoolException):
    def __init__(self, stat):
        Exception.__init__(self, 'Unknown stat picked for training: ' + stat)

class PetNotFoundException(IslandTrainingSchoolException):
    def __init__(self, pet_name):
        Exception.__init__(self, 'Pet was not found in training school: ' + pet_name)

class PetNotOnCourseException(IslandTrainingSchoolException):
    def __init__(self, pet_name):
        Exception.__init__(self, 'Pet is not on course in training school: ' + pet_name)

class PetAlreadyOnCourseException(IslandTrainingSchoolException):
    def __init__(self, pet_name):
        Exception.__init__(self, 'Pet is already on a course in training school: ' + pet_name)

class StatTooHighException(IslandTrainingSchoolException):
    def __init__(self, pet_name):
        Exception.__init__(self, 'Pet has too high stats, train level first: ' + pet_name)