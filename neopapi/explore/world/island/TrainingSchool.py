from neopapi.explore.world.island.Exceptions import UnknownStatException,\
    PetNotFoundException, PetNotOnCourseException, PetAlreadyOnCourseException
from neopapi.core.browse import register_page
from neopapi.core.browse.Browser import BROWSER
import re

"""
This module provides the API for the Mystery Island Training school

"""

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
    
    infos = page.find('b', text='Current Course Status').find_next().find_all('b')
    info = {}
    info['level'] = int(infos[1].text)
    info['strength'] = int(infos[2].text)
    info['defence'] = int(infos[3].text)
    info['movement'] = int(infos[4].text)
    info['current_hp'] = int(infos[5].text.split(' / ')[0])
    info['hp'] = int(infos[5].text.split(' / ')[1])
    
    return info

def get_course_status(pet_name):
    page = BROWSER.goto('island/training.phtml?type=status')
    
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
    
    page = BROWSER.goto('island/training.phtml?type=courses')
    if page.find('select', {'name': 'pet_name'}).find('option', value=pet_name) is None:
        raise PetNotFoundException(pet_name)
    
    post_dict = {'course_type' : stat,
                 'pet_name' : pet_name,
                 'type' : 'start'}
    
    result_page = BROWSER.post('island/process_training.phtml', post_dict)
    
    if 'That pet is already doing a course' in result_page.text:
        BROWSER.back()
        raise PetAlreadyOnCourseException(pet_name)
    
    # TODO: check if everything went all right
    
    return result_page

def get_course_cost(pet_name):
    '''
    This method checks if the given pet is currently enrolled in a course that
    still needs to be payed at the given school. If this is the case, it will
    return an array of item names that are needed to pay for the course.
    Otherwise it returns None.
    '''
    page = BROWSER.goto('island/training.phtml?type=status')
    
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
    page = BROWSER.goto('island/training.phtml?type=status')
    
    pet_td = page.find('td', text=re.compile(pet_name + '.*'))
    if pet_td is None:
        raise PetNotFoundException(pet_name)
    
    status_td = pet_td.find_parent('tr').find_next_sibling('tr').find_all('td')[1]
    if not 'This course has not been paid for yet' in status_td.text:
        raise PetNotOnCourseException(pet_name)
    
    result_page = BROWSER.goto('island/process_training.phtml?type=pay&pet_name=' + pet_name)
    # TODO: check if everything went all right
    return result_page

def finish_course(pet_name):
    '''
    This method finishes the current course of the given pet if it is finished
    '''
    page = BROWSER.goto('island/training.phtml?type=status')
    
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