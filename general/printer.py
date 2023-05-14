def terminal_starter():
    import os
    import ctypes
    from matplotlib import colors
    from rgbprint import rgbprint, gradient_print
    os.system(" ")
    if os.name == "nt":
        ctypes.windll.kernel32.SetConsoleTitleW("ColorBin Discord Bot 1.0.0")
    try:
        with open(fr"{os.getcwd()}\general\banner.txt", "r") as banner:
            lines = banner.readlines()
            for line in lines:
                line += "\n"
            lines[1] = " " + lines[1]
            gradient_print(*lines[1::], start_color=colors.to_hex(lines[0].split(">")[0]), end_color=colors.to_hex(lines[0].split(">")[1].replace("\n", "")))
        print("\n")
        with open(fr"{os.getcwd()}\general\text.txt", "r") as text:
            printcolor = None
            lines = text.readlines()
            for line in lines:
                if "rgb" in line:
                    printcolor = line.split(">")[1].replace("\n", "")
                else:
                    rgbprint(line.replace("\n", ""), color=colors.to_hex(printcolor) if printcolor is not None else (200, 200, 200))
        rgbprint("", color=(200, 200, 200))
    except FileNotFoundError:
        rgbprint("File 'banner.txt' or 'text.txt' is not found! Reinstall files", color=(255, 0, 0))
        os.system("pause")
        exit(1)
