def terminal_starter():
    import os
    import ctypes

    class bcolors:
        HEADER = "\033[95m"
        OKBLUE = "\033[94m"
        OKCYAN = "\033[96m"
        OKGREEN = "\033[92m"
        WARNING = "\033[93m"
        FAIL = "\033[91m"
        ENDC = "\033[0m"
        BOLD = "\033[1m"
        UNDERLINE = "\033[4m"
    os.system(" ")
    if os.name == "nt":
        ctypes.windll.kernel32.SetConsoleTitleW("ColorBin Discord Bot 1.0.0")
    print(f"{bcolors.OKGREEN} ::::::::   ::::::::  :::        ::::::::  :::::::::  ::::::::: ::::::::::: ::::    :::{bcolors.ENDC}")
    print(f"{bcolors.OKGREEN}:+:    :+: :+:    :+: :+:       :+:    :+: :+:    :+: :+:    :+:    :+:     :+:+:   :+:{bcolors.ENDC}")
    print(f"{bcolors.OKGREEN}+:+        +:+    +:+ +:+       +:+    +:+ +:+    +:+ +:+    +:+    +:+     :+:+:+  +:+{bcolors.ENDC}")
    print(f"{bcolors.OKGREEN}+#+        +#+    +:+ +#+       +#+    +:+ +#++:++#:  +#++:++#+     +#+     +#+ +:+ +#+{bcolors.ENDC}")
    print(f"{bcolors.OKGREEN}+#+        +#+    +#+ +#+       +#+    +#+ +#+    +#+ +#+    +#+    +#+     +#+  +#+#+#{bcolors.ENDC}")
    print(f"{bcolors.OKGREEN}#+#    #+# #+#    #+# #+#       #+#    #+# #+#    #+# #+#    #+#    #+#     #+#   #+#+#{bcolors.ENDC}")
    print(f"{bcolors.OKGREEN} ########   ########  ########## ########  ###    ### ######### ########### ###    ####{bcolors.ENDC}")
    print("")
    print("")
    print(f"{bcolors.HEADER}Welcome! {bcolors.ENDC}")
    print(f"{bcolors.OKCYAN}Discord Bot run by @TheColorfulBin {bcolors.ENDC}")
    print(f"{bcolors.OKCYAN}------------ SESSION ------------{bcolors.ENDC}")
