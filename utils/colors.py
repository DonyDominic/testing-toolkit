class Color:
    """
    Collection of style flags, ANSI color codes, and RGB mappings used
    for terminal text formatting.
    """
    # Flags
    RESET = 0

    # Styles
    BOLD = 1 
    THIN = 2 

    # Foreground Colors
    FG_GREEN = 4 
    FG_RED   = 8   
    FG_GREY  = 16   

    _ANSI = {
        BOLD : '1',
        THIN : '22',

        FG_GREEN : '92',
        FG_RED   : '91',
        FG_GREY  : '90'
    }

    _RGB ={
        FG_GREEN: (0, 160, 0),       
        FG_RED:   (160, 0, 0),       
        FG_GREY:  (160, 160, 160),   
    }


def colorize(text: str, flags: int,truecolor:bool = True) -> str:
    """
    Returns the text wrapped with ANSI or RGB color escape sequences.

    Args:
        text (str): The text to format.
        flags (int): Bitmask flags specifying styles and colors.
        truecolor (bool, optional): If True, applies 24-bit RGB escape codes.
            Otherwise uses ANSI. Defaults to False.

    Returns:
        str: The formatted text with escape sequences.
    """
    if flags == Color.RESET:
        return text
    codes = []

    for flag,code in Color._ANSI.items():
        if flag in (Color.BOLD,Color.THIN):
            if flags & flag:
                codes.append(code)
    
    for flag in (Color.FG_GREEN,Color.FG_RED,Color.FG_GREY):
        if flags & flag:
            if truecolor:
                r,g,b = Color._RGB[flag]
                codes.append(f"38;2;{r};{g};{b}")
            else:
                codes.append(Color._ANSI[flag])
        
    combined_code = ';'.join(codes)
    ANSI_START = '\033['
    ANSI_END   = 'm'
    RESET      = '\033[0m'

        
    return f"{ANSI_START}{combined_code}{ANSI_END}{text}{RESET}"

def _print_detail(value, flags):
    print(colorize(f"  {value}", flags))
