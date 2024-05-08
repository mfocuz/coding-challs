import json
from json import JSONDecodeError, loads, dumps
from binascii import hexlify, unhexlify
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from pwn import xor

# with open("flag") as f:
#     flag = f.readline()
flag = "IRISCTF{HERE_IS_YOUR_FLAG}"

key = get_random_bytes(16)


def encrypt(plaintext: bytes) -> (bytes, bytes):
    iv = get_random_bytes(16)
    aes = AES.new(key, AES.MODE_CBC, iv)
    # print("IV:", hexlify(iv).decode())
    return iv, aes.encrypt(plaintext)


def decrypt(ciphertext: bytes, iv: bytes) -> bytes:
    aes = AES.new(key, AES.MODE_CBC, iv)
    return aes.decrypt(ciphertext)


def create_command(message: str) -> (str, str):
    payload = {"from": "guest", "act": "echo", "msg": message}
    payload = dumps(payload).encode()
    while len(payload) % 16 != 0:
        payload += b'\x00'
    iv, payload = encrypt(payload)
    return hexlify(iv).decode('utf-8'), hexlify(payload).decode('utf-8')


def run_command(iv: bytes, command: str):
    try:
        iv = unhexlify(iv)
        command = unhexlify(command)
        command = decrypt(command, iv)

        while command.endswith(b'\x00') and len(command) > 0:
            command = command[:-1]
    except:
        print("Failed to decrypt")
        return

    try:
        command = command.decode()
        command = loads(command)
    except UnicodeDecodeError:
        print(f"Failed to decode UTF-8: {hexlify(command).decode('UTF-8')}")
        return hexlify(command).decode('UTF-8')
    except JSONDecodeError:
        print(f"Failed to decode JSON: {command}")
        return command

    match command["act"]:
        case "echo":
            msg = command['msg']
            print(f"You received the following message: {msg}")
        case "flag":
            if command["from"] == "admin":
                print(f"Congratulations! The flag is: {flag}")
                return command
            else:
                print("You don't have permissions to perform this action")
        case action:
            print(f"Invalid action {action}")


def show_prompt():
    print("-" * 75)
    print("1. Create command")
    print("2. Run command")
    print("3. Exit")
    print("-" * 75)

    try:
        sel = input("> ")
        sel = int(sel)

        match sel:
            case 1:
                msg = input("Please enter your message: ")
                iv, command = create_command(msg)
                print(f"IV: {iv}")
                print(f"Command: {command}")
            case 2:
                iv = input("IV: ")
                command = input("Command: ")
                run_command(iv, command)
            case 3:
                exit(0)
            case _:
                print("Invalid selection")
                return
    except ValueError:
        print("Invalid selection")
    except:
        print("Unknown error")


def solution():
    print("Simulating input '1' for prompt (create command)")
    iv, vanilla_command = create_command("whatever")
    message = json.dumps({"from": "guest", "act": "echo", "msg": "whatever"})
    print("message=%s" % message)
    print("encrypted message=%s" % vanilla_command)
    solution_message = json.dumps({"from": "admin", "act": "flag", "msg": "whatever"})
    print(f"IV: {iv}")
    print(f"Encrypted Command: {vanilla_command}")

    print("Bitflipping field command in 'act', 'echo' -> 'flag'")
    bit_flip_vector = xor("echo", "flag")
    vanilla_command = bytes.fromhex(vanilla_command)
    start_index = message.find("echo") - 16
    print("Xoring c0S block with bit_flip_vector")
    vanilla_command = vanilla_command[0:start_index] \
                      + xor(bit_flip_vector, vanilla_command[start_index:start_index+len("echo")]) \
                      + vanilla_command[start_index+len("echo"):]
    print("Simulating input '2' for prompt (run command)")
    output = bytes.fromhex(run_command(iv, vanilla_command.hex()))
    print("Output after bitflip 'echo' -> 'flag': %s" % output)

    print("Bitflipping whole block p0 with IV modification IV = IV ^ p0' ^  solution_message[0:16]")
    iv = bytes.fromhex(iv)
    iv = xor(iv, xor(output[0:16], solution_message[0:16]))
    print("Simulating input '2' for prompt again (run command)")
    output = run_command(iv.hex(), vanilla_command.hex())
    print("Output after bitflip whole IV and making 'guest'->'admin': %s" % output)


if __name__ == "__main__":
    solution()
