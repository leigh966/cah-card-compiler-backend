import uuid
import dbOperations
import authorization

def create_group(group_name):
    # generate game_id
    group_id = uuid.uuid4()
    # create group with name [group_name]
    dbOperations.create_record('groups', 'group_id,group_name', f"'{str(group_id)}','{group_name}'")
    # return game_id
    return group_id

def name_taken_in_group(name, group_id):
    where = f"contributer_name='{name}' AND group_id='{group_id}'"
    search = dbOperations.select('*', 'contributers', where)
    return len(search) > 0

def register_contributer(contributer_name, contributer_password, group_id):
    if name_taken_in_group(contributer_name, group_id):
        raise ValueError('That username is taken in this group')

    # if the group_id does not exist
        # raise a key error
    where = f"group_id='{group_id}'"
    if len(dbOperations.select('*', 'groups', where))==0:
        raise KeyError('This group does not exist')
    # hash password
    hashed_password = authorization.hash_password(contributer_password)
    # register new contributer with name [contributer_name], 
    #   password_hash [hashed_password] and group_id [group_id]
    fields = 'contributer_name,password_hash,group_id'
    values = f"'{contributer_name}','{str(hashed_password)}','{group_id}'"
    dbOperations.create_record('contributers', fields, values)
    

def add_card(card_text, contributer_id):
    # if contributer does not exists
        # raise not found error
    where = f"contributer_id='{contributer_id}'"
    if len(dbOperations.select('*', 'contributers', where))==0:
        raise KeyError('This contributer does not exist')
    # add a new card with card_text [card_text] and contributer_id [contributer_id]
    fields = 'card_text,contributer_id'
    values = f"'{card_text}','{contributer_id}'"
    dbOperations.create_record('cards', fields, values)

def get_my_cards(contributer_id):
    # assumes that the contributer_id is valid
    where = f"contributer_id='{contributer_id}'"
    cards = dbOperations.select('card_id,card_text', 'cards', where)
    return [{'card_id': record[0], 'card_text': record} for record in cards]
    
def get_group_name(group_id):
    where = f"group_id='{group_id}'"
    names = dbOperations.select("group_name", "groups", where)
    if len(names) == 0:
        return None
    return names[0][0]