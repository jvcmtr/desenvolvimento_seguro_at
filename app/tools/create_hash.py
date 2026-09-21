from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def hash_pass(password):
    return pwd_context.hash(password)

if __name__ == "__main__":
    password = input("Senha: ")
    hashed = hash(password)

    print("\nHash:")
    print('"' + hashed + '"')