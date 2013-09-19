from neopapi.world.island.Exceptions import UnknownStatException,\
    PetNotFoundException, PetNotOnCourseException
from neopapi.core.browse import register_page
from neopapi.core.browse.Browser import BROWSER
import re

register_page('island/training.phtml',
              ['island/training.phtml?type=status', 'island/training.phtml?type=courses'])
register_page('island/training.phtml?type=status',
              ['island/training.phtml?type=status', 'island/training.phtml?type=courses'])
register_page('island/training.phtml?type=courses',
              ['island/training.phtml?type=status', 'island/training.phtml?type=courses'])

# Stats to train
STATS = ['Level', 'Endurance', 'Strength', 'Defence', 'Agility']
LEVEL, HP, STRENGTH, DEFENCE, MOVEMENT = STATS
# Training statusses
IDLE, AWAITING_PAYMENT, TRAINING, FINISHED = 1, 2, 3, 4


def get_status(pet_name):
    '''
    Get the current status of the given pet in the island training school in the
    form of a dictionary
    '''
    page = BROWSER.goto('island/training.phtml?type=status')
    
    pet_td = page.find('td', text=re.compile(pet_name + '.*'))
    if pet_td is None:
        raise PetNotFoundException(pet_name)
    
    # FIXME: this probably doesn't work
    info_td = pet_td[:6]
    info = {}
    info['level'] = int(info_td[1].text)
    info['strength'] = int(info_td[2].text)
    info['defence'] = int(info_td[3].text)
    info['movement'] = int(info_td[4].text)
    info['current_hp'] = int(info_td[5].text.split(' / ')[0])
    info['hp'] = int(info_td[5].text.split(' / ')[1])
    
    return info

def get_course_status(pet_name):
    BROWSER.goto(__name__)
    page = BROWSER.get('island/training.phtml?type=status')
    
    pet_td = page.find('td', text=re.compile(pet_name + '.*'))
    if pet_td is None:
        raise PetNotFoundException(pet_name)
    
    status_td = pet_td.find_parent('tr').find_next_sibling('tr').find_all('td')[1]
    if status_td.text == 'Course Finished!':
        return FINISHED
    elif 'This course has not been paid for yet' in status_td.text:
        return AWAITING_PAYMENT
    elif 'Time till course finishes' in status_td.text:
        return TRAINING
    return IDLE

def start_course(pet_name, stat):
    '''
    This method starts a course for the given pet in the given stat
    '''
    if not stat in STATS:
        raise UnknownStatException(stat)
    
    BROWSER.goto(__name__)
    page = BROWSER.get('island/training.phtml?type=courses')
    
    # TODO: check if pet_name is available, if not raise PetNotFoundException
    
    post_dict = {'course_type' : stat,
                 'pet_name' : pet_name,
                 'type' : 'start'}
    
    result_page = BROWSER.post('island/process_training.phtml', post_dict)
    # TODO: check if everything went all right
    return result_page

def get_course_cost(pet_name):
    '''
    This method checks if the given pet is currently enrolled in a course that
    still needs to be payed at the given school. If this is the case, it will
    return an array of item names that are needed to pay for the course.
    Otherwise it returns None.
    '''
    BROWSER.goto(__name__)
    page = BROWSER.get('island/training.phtml?type=status')
    
    pet_td = page.find('td', text=re.compile(pet_name + '.*'))
    if pet_td is None:
        raise PetNotFoundException(pet_name)
    
    status_td = pet_td.find_parent('tr').find_next_sibling('tr').find_all('td')[1]
    if not 'This course has not been paid for yet' in status_td.text:
        raise PetNotOnCourseException(pet_name)
    
    return [tag.text for tag in status_td.find('p').find_all('b')]

def pay_course(pet_name):
    '''
    This method tries to pay the current course of the given pet.
    '''
    BROWSER.goto(__name__)
    page = BROWSER.get('island/training.phtml?type=status')
    
    pet_td = page.find('td', text=re.compile(pet_name + '.*'))
    if pet_td is None:
        raise PetNotFoundException(pet_name)
    
    status_td = pet_td.find_parent('tr').find_next_sibling('tr').find_all('td')[1]
    if not 'This course has not been paid for yet' in status_td.text:
        raise PetNotOnCourseException(pet_name)
    
    result_page = BROWSER.get('island/process_training.phtml?type=pay&pet_name=' + pet_name)
    # TODO: check if everything went all right
    return result_page

def finish_course(pet_name):
    '''
    This method finishes the current course of the given pet if it is finished
    '''
    BROWSER.goto(__name__)
    page = BROWSER.get('island/training.phtml?type=status')
    
    pet_td = page.find('td', text=re.compile(pet_name + '.*'))
    if pet_td is None:
        raise PetNotFoundException(pet_name)
    
    status_td = pet_td.find_parent('tr').find_next_sibling('tr').find_all('td')[1]
    if not 'Course Finished!' in status_td.text:
        raise PetNotOnCourseException(pet_name)
    
    post_dict = {'pet_name': pet_name,
                 'type': 'complete'}
    result_page = BROWSER.post('island/process_training.phtml', post_dict)
    # TODO: check if everything went all right
    return result_page