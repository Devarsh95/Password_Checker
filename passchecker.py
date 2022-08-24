import requests
import hashlib
import sys


def request_api_data(guery_char):
    url = 'https://api.pwnedpasswords.com/range/' + guery_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching:{res.status_code},check API and Try again')
    return res


def count_password_breached(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for has, count in hashes:
        if has == hash_to_check:
            return count
    return 0


def check_pass(password):
    sha1password = (hashlib.sha1(password.encode("UTF-8")).hexdigest().upper())
    first5_char, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first5_char)
    print(response)
    return count_password_breached(response, tail)


def main():
    with open('passkeeper.txt', 'r') as f:
        password_list = []
        for line in f:
            content = line.strip()
            password_list.append(content)

        for password in password_list:
            count = check_pass(password)
            if count:
                print(f'{password} found {count} many times, //Unsafe password ,CHANGE_PASSWORD  //')
            else:
                print(f'{password} is not found, // SAFE_PASSWORD //')
        print('Search completed!')

    # for password in args:
    #     count = pwned_api_check(password)
    #     if count:
    #         print(f'{password} was found {count} Times //Unsafe password ,CHANGE_PASSWORD  // ')
    #     else:
    #         print(f'{password} was not found,// SAFE_PASSWORD //')
    # return 'Password Check Done'


# request_api_data('123')
if __name__ == '__main__':
    main()
