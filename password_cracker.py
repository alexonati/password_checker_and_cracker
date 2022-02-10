import itertools
import random
import string
import timeit
import numpy as np

allowed_chars = string.ascii_lowercase + " "
password_database = {"alex": "my password is easy to guess"}


# Password cracker - if division by 0 error occurs, rerun the script. It just means that the random guessed length number of the password is 0.
def check_password(user, guess):
    actual = password_database[user]
    if len(guess) != len(actual):
        return False

    for i in range(len(actual)):
        if guess[i] != actual[i]:
            return False
    return True


def random_str(size):
    return ''.join(random.choices(allowed_chars, k=size))


def crack_length(user, max_len=32, verbose=False) -> int:
    trials = 1000
    times = np.empty(max_len)
    for i in range(max_len):
        i_time = timeit.repeat(stmt='check_password(user, x)',
                               setup=f'user={user!r};x=random_str({i!r})',
                               globals=globals(),
                               number=trials,
                               repeat=10)
        times[i] = min(i_time)

    if verbose:
        most_likely_n = np.argsort(times)[::-1][:5]
        print(most_likely_n, times[most_likely_n] / times[most_likely_n[0]])

    most_likely = int(np.argmax(times))
    return most_likely


def crack_password(user, length, verbose=False):
    guess = random_str(length)
    counter = itertools.count()
    trials = 10000
    while True:
        i = next(counter) % length
        for c in allowed_chars:
            alt = guess[:i] + c + guess[i + 1:]

            alt_time = timeit.repeat(stmt='check_password(user, x)',
                                     setup=f'user={user!r};x={alt!r}',
                                     globals=globals(),
                                     number=trials,
                                     repeat=10)
            guess_time = timeit.repeat(stmt='check_password(user, x)',
                                       setup=f'user={user!r};x={guess!r}',
                                       globals=globals(),
                                       number=trials,
                                       repeat=10)

            if check_password(user, alt):
                return alt

            if min(alt_time) > min(guess_time):
                guess = alt
                if verbose:
                    print(guess)


def main():
    user = "alex"
    length = crack_length(user, verbose=True)
    print(f"Most likely length {length}")
    input("Enter to continue...")
    password = crack_password(user, length, verbose=True)
    print(f"password cracked:'{password}'")


if __name__ == '__main__':
    main()
