import time
try:
    from colorama import Fore, Style
except ImportError:
    print("colorama package not installed\nRun the installer")
    time.sleep(2)
    exit(0)


main_banner = (
    Style.BRIGHT + Fore.RED + """\n\t\t
                    ██╗███╗   ███╗ █████╗  ██████╗ ███████╗    ███████╗██╗   ██╗███╗   ██╗████████╗██╗  ██╗██╗  ██╗
                    ██║████╗ ████║██╔══██╗██╔════╝ ██╔════╝    ██╔════╝╚██╗ ██╔╝████╗  ██║╚══██╔══╝██║  ██║╚██╗██╔╝
                    ██║██╔████╔██║███████║██║  ███╗█████╗█████╗███████╗ ╚████╔╝ ██╔██╗ ██║   ██║   ███████║ ╚███╔╝ 
                    ██║██║╚██╔╝██║██╔══██║██║   ██║██╔══╝╚════╝╚════██║  ╚██╔╝  ██║╚██╗██║   ██║   ██╔══██║ ██╔██╗ 
                    ██║██║ ╚═╝ ██║██║  ██║╚██████╔╝███████╗    ███████║   ██║   ██║ ╚████║   ██║   ██║  ██║██╔╝ ██╗
                    ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝    ╚══════╝   ╚═╝   ╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝
                                                                                                \n"""
    + Fore.CYAN + """\n\t\t[1]""" + Fore.MAGENTA + """ Web Interface""" + Fore.BLUE + """ (WEB-UI)""" +
    Fore.CYAN + """\n\t\t[2]""" + Fore.GREEN + """ Image upscaler""" + Fore.YELLOW + """ (REAL ESRGAN)""" +
    Fore.CYAN + """\n\t\t[3]""" + Fore.GREEN + """ Text to image""" + Fore.YELLOW + """ (SDXL)""" +
    Fore.CYAN + """\n\t\t[4]""" + Fore.GREEN + """ Text to image generation""" + Fore.YELLOW + """ (HIGH RES CARTOON)(LATENT-CONSISTENCY-MODEL)""" +
    Fore.CYAN + """\n\t\t[5]""" + Fore.GREEN + """ Anime""" + Fore.YELLOW + """ (ANYTHING V4.0) -> MAX RES: [1024x768 or 768x1024]""" +
    Fore.CYAN + """\n\t\t[C]""" + Fore.GREEN + """ Credits""" +
    Fore.CYAN + """\n\t\t[0]""" + Fore.GREEN + """ EXIT
    """)


credits_banner = (Fore.RED + """
                         ██████╗██████╗ ███████╗██████╗ ██╗████████╗███████╗
                        ██╔════╝██╔══██╗██╔════╝██╔══██╗██║╚══██╔══╝██╔════╝
                        ██║     ██████╔╝█████╗  ██║  ██║██║   ██║   ███████╗
                        ██║     ██╔══██╗██╔══╝  ██║  ██║██║   ██║   ╚════██║
                        ╚██████╗██║  ██║███████╗██████╔╝██║   ██║   ███████║
                        ╚═════╝╚═╝  ╚═╝╚══════╝╚═════╝ ╚═╝   ╚═╝   ╚══════╝
                                                    
                                         Image-SynthX\n""" + Fore.BLUE + """
                                  Programming:""" + Fore.CYAN + """ Naveen William""")


anything_banner = Style.BRIGHT + Fore.MAGENTA + """\n
                    █████╗ ███╗   ██╗██╗   ██╗████████╗██╗  ██╗██╗███╗   ██╗ ██████╗     ██╗   ██╗██╗  ██╗    ██████╗ 
                    ██╔══██╗████╗  ██║╚██╗ ██╔╝╚══██╔══╝██║  ██║██║████╗  ██║██╔════╝     ██║   ██║██║  ██║   ██╔═████╗
                    ███████║██╔██╗ ██║ ╚████╔╝    ██║   ███████║██║██╔██╗ ██║██║  ███╗    ██║   ██║███████║   ██║██╔██║
                    ██╔══██║██║╚██╗██║  ╚██╔╝     ██║   ██╔══██║██║██║╚██╗██║██║   ██║    ╚██╗ ██╔╝╚════██║   ████╔╝██║
                    ██║  ██║██║ ╚████║   ██║      ██║   ██║  ██║██║██║ ╚████║╚██████╔╝     ╚████╔╝      ██║██╗╚██████╔╝
                    ╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝      ╚═╝   ╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝       ╚═══╝       ╚═╝╚═╝ ╚═════╝ 
    \n"""


lcm_banner = Style.BRIGHT + Fore.MAGENTA + """\n
                                                    ██╗      ██████╗███╗   ███╗
                                                    ██║     ██╔════╝████╗ ████║
                                                    ██║     ██║     ██╔████╔██║
                                                    ██║     ██║     ██║╚██╔╝██║
                                                    ███████╗╚██████╗██║ ╚═╝ ██║
                                                    ╚══════╝ ╚═════╝╚═╝     ╚═╝
    \n"""


sdxl_banner = Style.BRIGHT + Fore.MAGENTA + """\n
                                                    ███████╗██████╗ ██╗  ██╗██╗     
                                                    ██╔════╝██╔══██╗╚██╗██╔╝██║     
                                                    ███████╗██║  ██║ ╚███╔╝ ██║     
                                                    ╚════██║██║  ██║ ██╔██╗ ██║     
                                                    ███████║██████╔╝██╔╝ ██╗███████╗
                                                    ╚══════╝╚═════╝ ╚═╝  ╚═╝╚══════╝
    \n"""


esrgan_banner = Style.BRIGHT + Fore.MAGENTA + """\n
                        ██████╗ ███████╗ █████╗ ██╗         ███████╗███████╗██████╗  ██████╗  █████╗ ███╗   ██╗
                        ██╔══██╗██╔════╝██╔══██╗██║         ██╔════╝██╔════╝██╔══██╗██╔════╝ ██╔══██╗████╗  ██║
                        ██████╔╝█████╗  ███████║██║         █████╗  ███████╗██████╔╝██║  ███╗███████║██╔██╗ ██║
                        ██╔══██╗██╔══╝  ██╔══██║██║         ██╔══╝  ╚════██║██╔══██╗██║   ██║██╔══██║██║╚██╗██║
                        ██║  ██║███████╗██║  ██║███████╗    ███████╗███████║██║  ██║╚██████╔╝██║  ██║██║ ╚████║
                        ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚══════╝    ╚══════╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝
    \n
    """


images_banner = Style.BRIGHT + Fore.RED + """
        ██╗███╗   ███╗ █████╗  ██████╗ ███████╗███████╗
        ██║████╗ ████║██╔══██╗██╔════╝ ██╔════╝██╔════╝
        ██║██╔████╔██║███████║██║  ███╗█████╗  ███████╗
        ██║██║╚██╔╝██║██╔══██║██║   ██║██╔══╝  ╚════██║
        ██║██║ ╚═╝ ██║██║  ██║╚██████╔╝███████╗███████║
        ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚══════╝
    """