from auth import *

def main():
    password = "P@ss123456"
    hashed_password = hash_password(password)
    print(f"hash: {hashed_password}")
    print(f"verify ok: {verify_password(password, hashed_password)}")
    print(f"verify bad: {verify_password("P@ass1234567", hashed_password)}")

    token = create_access_token(sub="zamanov@itstep.org", role="admin")
    print(f"token: {token}")
    print(f"payload: {decode_token(token)}")

if __name__ == "__main__":
    main()