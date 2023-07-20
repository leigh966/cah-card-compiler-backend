import uuid
import dbOperations
import authorization

def create_group(group_name):
    # generate game_id
    group_id = uuid.uuid4()
    # create group with name [group_name]
    dbOperations.create_record("groups", "group_id,group_name", f'"{str(group_id)}","{group_name}"')
    # return game_id
    return group_id

def register_contributer(contributer_name, contributer_password, group_id):
    # assumes contributer name is unique
    # if the group_id does not exist
        # raise a key error
    where = f'group_id="{group_id}"'
    if len(dbOperations.select("*", "groups", where))==0:
        raise KeyError("This group does not exist")
    # hash password
    hashed_password = authorization.hash_password(contributer_password)
    # register new contributer with name [contributer_name], 
    #   password_hash [hashed_password] and group_id [group_id]
    fields = "contributer_name,password_hash,group_id"
    values = f'"{contributer_name}","{str(hashed_password)}","{group_id}"'
    dbOperations.create_record("contributers", fields, values)
    

def add_card(card_text, contributer_id):
    # if contributer does not exists
        # raise not found error
    where = f'contributer_id="{contributer_id}"'
    if len(dbOperations.select("*", "contributers", where))==0:
        raise KeyError("This contributer does not exist")
    # add a new card with card_text [card_text] and contributer_id [contributer_id]
    fields = "card_text,contributer_id"
    values = f'"{card_text}","{contributer_id}"'
    dbOperations.create_record("cards", fields, values)