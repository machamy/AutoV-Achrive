import keyboard

from v_archive import User
import djmax
import time
import asyncio

def main():
    screen = djmax.Screen(1,"DJMAX RESPECT V")
    screen.start()

    while not keyboard.is_pressed('Q'):
        time.sleep(1)
    screen.end()

# bepo = User("김베포")
# bepo.refresh(6, 10)
# print('\n\n\n\n')
# bepo.refresh(6, 11)


if __name__ == '__main__':
    main()