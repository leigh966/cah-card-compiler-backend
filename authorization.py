from passlib.hash import pbkdf2_sha256
import dbOperations
import uuid

def hash_password(password):
  """Hash the password using PBKDF2 with SHA-256."""
  return pbkdf2_sha256.hash(password)

def check_password(password, hashed_password):
  """Check if the entered password matches the stored hashed password."""
  return pbkdf2_sha256.verify(password, hashed_password)

def get_user_id(session_id):
  where = f'session_id="{session_id}"'
  return dbOperations.select("contributer_id", "sessions", where)[0][0]

def login(username, password, group_id):
  where = f"group_id='{group_id}' AND contributer_name='{username}'"
  user = dbOperations.select("contributer_id,password_hash", "contributers", where)[0]
  if not check_password(password, user[1]):
    raise ValueError("Incorrect Password")
  session_id = str(uuid.uuid4())
  fields = "session_id,contributer_id"
  values = f"'{session_id}',{user[0]}"
  dbOperations.create_record("sessions", fields, values)
  return session_id
  