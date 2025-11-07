import curses 

stdscr = curses.initscr()

def new_menu(title, classes, color='green', return_as='index'):
# define the curses wrapper
  def character(stdscr,):
    attributes = {}
    # stuff i copied from the internet that i'll put in the right format later
    icol = {
      1:'red',
      2:'green',
      3:'yellow',
      4:'blue',
      5:'magenta',
      6:'cyan',
      7:'white'
    }
    # put the stuff in the right format
    col = {v: k for k, v in icol.items()}

    # declare the background color

    bc = curses.COLOR_BLACK

    # make the 'normal' format
    curses.init_pair(1, 7, bc)
    attributes['normal'] = curses.color_pair(1)


    # make the 'highlighted' format
    curses.init_pair(2, col[color], bc)
    attributes['highlighted'] = curses.color_pair(2)


    # handle the menu
    c = 0
    option = 0
    while c != 10:

        stdscr.erase() # clear the screen (you can erase this if you want)

        # add the title
        stdscr.addstr(f"{title}\n", curses.color_pair(1))

        # add the options
        for i in range(len(classes)):
            # handle the colors
            if i == option:
                attr = attributes['highlighted']
            else:
                attr = attributes['normal']
            
            # actually add the options

            stdscr.addstr(f'> ', attr)
            stdscr.addstr(f'{classes[i]}' + '\n', attr)
        c = stdscr.getch()

        # handle the arrow keys
        KEY_UP = 450
        KEY_DOWN = 456
        if c == KEY_UP:
            if option > 0:
              option -= 1
            else:
               option = len(classes) -1
        elif c == KEY_DOWN:
            if option < len(classes) - 1:
              option += 1
            else:
              option = 0
    if return_as == 'index':
       return option
    elif return_as == 'raw':
        return classes[option]
  return curses.wrapper(character)

def new_text_display(classes):
  stdscr.erase()
  def character(stdscr,):
        for i in range(len(classes)):
            stdscr.addstr(f'{classes[i]}\n', curses.color_pair(1))
        stdscr.getch()
  return curses.wrapper(character)
   