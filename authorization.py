from passlib.hash import pbkdf2_sha256

def hash_password(password):
  """Hash the password using PBKDF2 with SHA-256."""
  return pbkdf2_sha256.hash(password)

def check_password(password, hashed_password):
  """Check if the entered password matches the stored hashed password."""
  return pbkdf2_sha256.verify(password, hashed_password)
